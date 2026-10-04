Doporučuji nechat všechny presety v `regex`, ze `patterns` odstranit ty, které se překrývají, a nechat `patterns` je jen znovu vystavit. Závislost jde totiž jedním směrem: `patterns` staví na `regex`, takže společná věc se musí definovat v `regex`. Opačně by vznikla cyklická závislost.

## Dělení rolí

- **`regex` je vrstva syntaxe.** Obsahuje to, co umí regulární výraz sám o sobě, bez znalosti oboru: kotvy, `ANY`, znakové typy (`\d`, `\w`…), skupiny, lookaroundy, kvantifikátory, a k tomu základní třídy znaků a řídicí znaky.
- **`patterns` je vrstva významu.** Obsahuje pojmenované věci z reálného světa (`EMAIL`, `ISO_DATE`, `URL`…) a staví je z presetů `regex`.

Test, kterým se rozhodnu: dá se `regex` používat samostatně, bez `patterns`? Dá, ale jen pokud má základní znaky (`HEX_DIGIT`, `TAB`…) u sebe. Proto nedoporučuji přesouvat `character_classes` a `literals` do `patterns`. Byly by pak dostupné jen s druhou knihovnou a navíc je máš v 0.1.0 zveřejněné, takže by šlo o zbytečně rozbitou změnu.

## Překryv

| Situace | Presety |
|---|---|
| Stejné jméno, stejný význam (nejspíš) | `DIGIT`, `NON_DIGIT`, `WHITESPACE`, `NON_WHITESPACE`, `HEX_DIGIT`, `LETTER`, `LOWERCASE_LETTER`, `UPPERCASE_LETTER`, `ALPHANUMERIC`, `TAB`, `NEWLINE`, `CARRIAGE_RETURN`, `FORM_FEED` |
| **Stejné jméno, jiný význam** | `WORD`: v `regex` znak `\w`, v `patterns` celé slovo |
| Stejný význam, jiné jméno | `WORD` / `NON_WORD` (regex) = `WORD_CHARACTER` / `NON_WORD_CHARACTER` (patterns); `BACKSLASH_CHAR` (regex) = `BACKSLASH` (patterns) |
| Jen v `regex` | kotvy, `ANY`, skupiny, lookaroundy, kvantifikátory, `BELL`, `VERTICAL_TAB` |

Slovo „nejspíš“ u první řádky je důležité. Nevidím definice ve `patterns`. Pokud se u některého presetu liší vykreslený vzor (třeba `DIGIT` jako `[0-9]` oproti `\d`, nebo ASCII oproti Unicode u `LETTER`), není to duplicita, ale dvě různé věci pod stejným jménem, a to je potřeba rozhodnout dřív, než se cokoli smaže.

## Pravidla, která navrhuji

1. **Jedna definice, jeden objekt.** Přesahující presety `patterns` nedefinuje, jen je importuje z `regex`. Tím je `patterns.DIGIT is regex.DIGIT` pravda a oprava se dělá na jednom místě.
2. **`patterns` vystaví všechny presety z `regex`**, tak jak chceš: kdo si nainstaluje jen `patterns`, nemusí vědět, odkud co importovat. Je to levné a pro uživatele pohodlné. Doporučuji ale soubor `_regex_presets.py`, kde je to všechno na jednom místě. Když `regex` něco přejmenuje, upraví se jedno místo.
3. **Při kolizi jmen vyhrává `patterns`.** `WORD` ve `patterns` zůstává slovem, a `\w` je dostupné jako `WORD_CHARACTER`, který už máš. Do README `patterns` patří jedna věta, že `WORD` je tam slovo, ne znak. Přejmenovat `WORD` v `regex` nechci, protože odpovídá syntaxi `\w` a je v publikované 0.1.0.
4. **`BACKSLASH` oproti `BACKSLASH_CHAR`:** nech obojí. `patterns.BACKSLASH` může být prostě `regex.BACKSLASH_CHAR` pod jiným jménem.
5. **Hlídací test ve `patterns`:** pro každý preset z `regex` ověřit, že `patterns.X is regex.X`, s výjimkou explicitního seznamu (`WORD`). Tím se tichá divergence nemůže vrátit.

## Co potřebuju, až se k tomu vrátíme

Definice těch 13 překrývajících se presetů z `patterns` (stačí vykreslený vzor každého) a aktuální `__init__.py` obou knihoven. Z toho vyrobím přesný seznam „smazat / nahradit importem / nechat“.

Jedna nesouvisející poznámka k `__all__` ve `patterns`: obsahuje `"Language"` s velkým počátečním písmenem mezi samými konstantami. Zkontroluj, jestli to je záměr, nebo třída, která se tam dostala omylem.