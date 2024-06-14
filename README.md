<div align="center">
  <p>
    <a href="#"><img src="https://raw.githubusercontent.com/Halvani/alphabetic/main/assets/images/logo.jpg" alt="Alphabetic logo"/></a>
  </p>
  <p align="center">
    <a href="https://pypi.org/project/alphabetic/"><img src="https://img.shields.io/pypi/v/alphabetic?style=flat-square"/></a>
	<a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"/></a>
  <a href="https://pypi.org/project/alphabetic"><img src="https://img.shields.io/pypi/pyversions/alphabetic.svg"/></a>
    <a href="https://github.com/Halvani/alphabetic/actions/workflows/python-package.yml"><img src="https://github.com/Halvani/alphabetic/actions/workflows/python-package.yml/badge.svg"/></a>
    <a href="https://github.com/Halvani/alphabetic"><img src="https://img.shields.io/github/last-commit/Halvani/alphabetic"/></a>
    <a href="https://doi.org/10.5281/zenodo.11580510"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.11580510.svg"/></a>
  </p>
</div>

# Alphabetic
A Python module for retrieving script types of writing systems including alphabets, abjads, abugidas, syllabaries, logographs, featurals as well as Latin script codes.

## Description / Background
Alphabetic is a small project that was born out of the need to find out the alphabet of different languages for a private NLP project. Determining the alphabet (or other script types) of a language plays an important role in a variety of NLP tasks and can be used, for example, to classify the language of a given text, normalize it by removing noisy/random strings, apply fine-grained regex pattern matching, and more.  

Core functionality in a nutshell: given a [specific language](#Supported_Languages) Alphabetic, first translates its name internally into a corresponding ISO code (either [ISO 639-2/3](https://www.loc.gov/standards/iso639-2/php/code_list.php) or [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924)) and outputs the corresponding script, which is categorized according to the writing systems listed in the following table (adapted from [here](https://en.wikipedia.org/wiki/Writing_system)):

|Writing system|Each symbol represents|Example|
|---|---|---|
|[Abjad](https://en.wikipedia.org/wiki/Abjad)|Consonant|Arabic alphabet|
|[Abugida](https://en.wikipedia.org/wiki/Abugida)|Consonant accompanied by specific vowel modifying symbols represent other vowels|Indian Devanagari|
|[Alphabet](https://en.wikipedia.org/wiki/Alphabet)|Consonant or vowel|Latin alphabet|
|[Featural system](https://en.wikipedia.org/wiki/Featural_writing_system)|Distinctive feature of segment|Korean Hangul|
|[Logographic](https://en.wikipedia.org/wiki/Logogram)|Word or morpheme as well as syllable|Chinese characters|
|[Syllabary](https://en.wikipedia.org/wiki/Syllabary)|Syllable|Japanese kana|

The distinction between the different script types is important in this respect and necessary in certain application scenarios, as otherwise it can lead to unexpected behavior. Perhaps you have already worked with the built-in string functions in Python? If so, you may have noticed the following questionable result: 
```python
print("伏伐休众优伙".isalpha())

# True
```
The answer ```True``` could be interpreted as meaning that the string, which is written in Chinese, is **alphabetic**. From a linguistic point of view, however, this is incorrect, as [there is no alphabet](https://www.berlitz.com/blog/chinese-alphabet) in Chinese (the Chinese writing system is [logographic](https://en.wikipedia.org/wiki/Simplified_Chinese_characters)). On the other hand, the following string, which is written in the Devanagari script, is in fact [not an alphabet but an abugida](https://en.wikipedia.org/wiki/Devanagari):
```python
print("अमित".isalpha())
       
# False
```
For this and other [use cases](#Usage) Alphabetic can be employed.   

## Installation
The easiest way to install Alphabetic is to use pip, where you can choose between PyPI and this repository: 

- ```pip install alphabetic```
- ```pip install git+https://github.com/Halvani/alphabetic.git```

The latter will pull and install the latest commit from this repository as well as the required Python dependencies. Note that the repo is updated regulary, while PyPi-packages are less frequently released (primarily after mayor bugfixing, refactoring, etc.).

<a name="Usage"></a>
## Usage
A simple lookup of a language's script (e.g., alphabet) can be performed as follows:
```python
from alphabetic import WritingSystem

ws = WritingSystem()
ws.by_language(ws.Language.Hawaiian)

# {"Hawaiian": ["A", "E", "H", "I", "K", "L", "M", "N", "O", "P", "U", "W", "a", "e", "h", "i", "k", "l", "m", "n", "o", "p", "u", "w", "ʻ"]}
```
By default, the output of ```by_language``` is a dictionary containing the name and the corresponding script of the [selected language](#Supported_Languages). To retrieve only the latter, use ```ws.by_language(ws.Language.Hawaiian, as_list=True)```. However, some languages such as Japanese have not one but [multiple writing systems](https://www.busuu.com/en/japanese/alphabet). In such a case, the output would look like this: 
```python
ws.by_language(ws.Language.Japanese)

# {"Japanese": {"Hiragana": ["あ", "い", ...], "Kanji": ["万", "丁", ...], "Katakana": ["ア", "イ", ...]}}
```
In case you want a pretty print of the output, use: 

```python
ws.pretty_print(ws.by_language(ws.Language.Dutch))

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z
```
If the resulting script represents an alphabet, the result can be further filtered in terms of: 
- **Letter Casing**:
```python
ws.pretty_print(ws.by_language(ws.Language.Bosnian))

# Ђ Ј Љ Њ Ћ Џ А Б В Г Д Е Ж З И К Л М Н О П Р С Т У Ф Х Ц Ч Ш а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ђ ј љ њ ћ џ

ws.pretty_print(ws.by_language(ws.Language.Bosnian, letter_case=ws.LetterCase.Upper))

# Ђ Ј Љ Њ Ћ Џ А Б В Г Д Е Ж З И К Л М Н О П Р С Т У Ф Х Ц Ч Ш
```

- **Multigraphs**:
```python
ws.pretty_print(ws.by_language(ws.Language.Aleut))
      
# A B Ch D E F G H Hl Hm Hn Hng I J K L M N Ng O P Q R S T U Uu V W X X̂ Y Z a b ch d e f g h hl hm hn hng i j k l m n ng o p q r s t u uu v w x x̂ y z Á á Ĝ ĝ

ws.pretty_print(ws.by_language(ws.Language.Aleut, strip_multigraphs=True, multigraphs_size=ws.MultigraphSize.All))

# A B D E F G H I J K L M N O P Q R S T U V W X Y Z a b d e f g h i j k l m n o p q r s t u v w x y z Á á Ĝ ĝ
```

- **Diacritics**
```python
ws.pretty_print(ws.by_language(ws.Language.Czech))
                
# A B C C h D E F G H I J K L M N O P Q R S T U V W X Y Z a b c c h d e f g h i j k l m n o p q r s t u v w x y z Á É Í Ó Ú Ý á é í ó ú ý Č č Ď ď Ě ě Ň ň Ř ř Š š Ť ť Ů ů Ž ž

ws.pretty_print(ws.by_language(ws.Language.Czech, strip_diacritics=True))

# A B C C h D E F G H I J K L M N O P Q R S T U V W X Y Z a b c c h d e f g h i j k l m n o p q r s t u v w x y z
```
For certain languages such as Chinese (simplified), which have a language code but no alphabet, a fallback strategy is used which maps the ISO 639-2 language code to an ISO 15924 code (as an example here: "chi" --> "Hans"). As a user, you do not have to handle this manually, but simply call up the language as it is:

```python
ws.pretty_print(ws.by_language(ws.Language.Chinese_Simplified))

# 㑇 㑊 㕮 㘎 㙍 㙘 㙦 㛃 㛚 㛹 㟃 㠇 㠓 㤘 㥄 㧐 ...
```
Another important use case is to check whether a given sequence of characters represents a specific script of a writing system. This can be achieved as follows:
```python
ws.is_abjad("גדולים או בינוניים") # True
ws.is_alphabet("גדולים או בינוניים") # False

ws.is_alphabet("dobré ráno") # True
ws.is_abjad("dobré ráno") # False

ws.is_logographic("早上好") # True
ws.is_syllabary("早上好") # False

ws.is_abugida("ምልካም እድል") # True
ws.is_abjad("ምልካም እድል") # False

ws.is_featural("좋은 아침") # True
ws.is_logographic("좋은 아침") # False

ws.is_alphabet("დილა მშვიდობისა") # True
ws.is_abjad("დილა მშვიდობისა") # False
```

Furthermore, you can also use Alphabetic to remove all characters from a given string that do not occur within the supported script types (abjads, abugidas, alphabets, etc.):  

```python
ws.strip_non_script_characters("SΓpλrώaσcσhεeςn!", ws.Language.German)
# "Sprachen" (languages)

ws.strip_non_script_characters("SΓpλrώaσcσhεeςn!", ws.Language.Greek)
# "Γλώσσες" (languages)
```

If no language is given, all characters of all supported script types are considered:
```python
ws.strip_non_script_characters("#jüste BAD/good tösté X4567Y ßÜ משהו действует?!")
# Result: 'jüste BADgood tösté XY ßÜ משהו действует'
```

If you wish, you can also list the characters of a language based on a specified Unicode range:
```python
ws.generate_all_characters_in_range("\u0400-\u04FF") # Bulgarian

# ['Ѐ', 'Ё', 'Ђ', 'Ѓ', 'Є', ..., 'Ӽ', 'ӽ', 'Ӿ', 'ӿ']
```



## Features
- Currently [151 languages](#Supported_Languages) and corresponding scripts are supported, with more to follow over time;

- In total, Alphabetic covers six writing systems script types: [abjads](https://en.wikipedia.org/wiki/Abjad), [abugidas](https://en.wikipedia.org/wiki/Abugida), [alphabets](https://en.wikipedia.org/wiki/Alphabet), [syllabaries](https://en.wikipedia.org/wiki/Syllabary), [logographics](https://en.wikipedia.org/wiki/Logogram) as well as [featurals](https://en.wikipedia.org/wiki/Featural_writing_system);

- Beside (true) writing systems, Alphabetic also offers Latin script representations (e.g., [Morse](https://en.wikipedia.org/wiki/Morse_code) or [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet));

- Alphabetic includes a complete list of all ISO 639-1/2/3 as well as ISO 15924 codes and enables bidirectional translation between language names and codes;

- At the heart of Alphabetic are [json files](https://github.com/Halvani/alphabetic/blob/main/alphabetic/data) that can be used independently of the respective programming language or application;

- Consistently documented source code.


<a name="Supported_Languages"></a>
## Supported Languages
<details><summary>Open to view all supported languages</summary>

|Language|ISO 639-2/3 code|
|---|---|
|Abkhazian|abk|
|Afar|aar|
|Afrikaans|afr|
|Albanian|sqi|
|Aleut|ale|
|Amharic|amh|
|Angika|anp|
|Arabic|ara|
|Arapaho|arp|
|Armenian|arm|
|Assamese|asm|
|Avar|ava|
|Avestan|ave|
|Balochi|bal|
|Bambara|bam|
|Bashkir|bak|
|Basque|baq|
|Bavarian|bar|
|Belarusian|bel|
|Bislama|bis|
|Boko|bqc|
|Boro|brx|
|Bosnian|bos|
|Breton|bre|
|Bulgarian|bul|
|Buryat|bua|
|Catalan|cat|
|Chamorro|cha|
|Chechen|che|
|Cherokee|chr|
|Chichewa|nya|
|Chinese_Simplified|chi|
|Chukchi|ckt|
|Chuvash|chv|
|Cimbrian|cim|
|Cornish|cor|
|Corsican|cos|
|Cree|cre|
|Croatian|hrv|
|Czech|ces|
|Danish|dan|
|Dungan|dng|
|Dutch|nld|
|Dzongkha|dzo|
|Elfdalian|ovd|
|English|eng|
|Esperanto|epo|
|Estonian|est|
|Ewe|ewe|
|Faroese|fao|
|Fijian|fij|
|Finnish|fin|
|Flemish|dut|
|French|fra|
|Georgian|kat|
|German|deu|
|Greek|gre|
|Guarani|grn|
|Haitian_Creole|hat|
|Hausa|hau|
|Hawaiian|haw|
|Hebrew|heb|
|Herero|her|
|Hindi|hin|
|Icelandic|isl|
|Igbo|ibo|
|Indonesian|ind|
|Irish|gle|
|Istro_Romanian|ruo|
|Italian|ita|
|Japanese|jpn|
|Javanese|jav|
|Jeju|jje|
|Kabardian|kbd|
|Kanuri|kau|
|Kashubian|csb|
|Kazakh|kaz|
|Kinyarwanda|kin|
|Kirghiz|kir|
|Komi|kpv|
|Korean|kor|
|Kumyk|kum|
|Kurmanji|kmr|
|Latin|lat|
|Latvian|lav|
|Lezghian|lez|
|Lingala|lin|
|Lithuanian|lit|
|Luganda|lug|
|Luxembourgish|ltz|
|Macedonian|mkd|
|Malagasy|mlg|
|Malay|may|
|Malayalam|mal|
|Maltese|mlt|
|Manx|glv|
|Maori|mao|
|Mari|chm|
|Marshallese|mah|
|Moksha|mdf|
|Moldovan|rum|
|Mongolian|mon|
|Mru|mro|
|Nepali|nep|
|Norwegian|nor|
|Occitan|oci|
|Oromo|orm|
|Osage|osa|
|Parthian|xpr|
|Pashto|pus|
|Persian|per|
|Phoenician|phn|
|Polish|pol|
|Portuguese|por|
|Punjabi_Gurmukhī|_pan|
|Punjabi_Shahmukhi|pan|
|Quechua|que|
|Rohingya|rhg|
|Russian|rus|
|Samaritan|smp|
|Samoan|smo|
|Sango|sag|
|Sanskrit|san|
|Scottish_Gaelic|gla|
|Serbian|srp|
|Slovak|slo|
|Slovenian|slv|
|Somali|som|
|Sorani|ckb|
|Spanish|spa|
|Sundanese|sun|
|Swedish|swe|
|Swiss_German|gsw|
|Tajik|tgk|
|Tatar|tat|
|Turkish|tur|
|Turkmen|tuk|
|Tuvan|tyv|
|Twi|twi|
|Ugaritic|uga|
|Ukrainian|ukr|
|Uzbek|uzb|
|Venda|ven|
|Vengo|bav|
|Volapük|vol|
|Welsh|wel|
|Wolof|wol|
|Yakut|sah|
|Yiddish|yid|
|Zeeuws|zea|
|Zulu|zul|
</details>


<a name="Supported_Abjads"></a>
## Supported Abjads
<details><summary>Open to view all supported abjads</summary>

|Abjad|ISO code|
|---|---|
|Arabic|Arab|
|Balochi|bal|
|Hebrew|Hebr|
|Hebrew_Samaritan|Samr|
|Parthian|Prti|
|Pashto|pus|
|Persian|per|
|Phoenician|Phnx|
|Punjabi_Shahmukhi|pan|
|Sorani|ckb|
|Ugaritic|Ugar|
|Yiddish|yid|
</details>

<a name="Supported_Abugidas"></a>
## Supported Abugidas
<details><summary>Open to view all supported abugidas</summary>

|Abugida|ISO code|
|---|---|
|Amharic|amh|
|Angika|anp|
|Assamese|asm|
|Boro|brx|
|Devanagari|Deva|
|Dzongkha|dzo|
|Ethiopic|Ethi|
|Hindi|hin|
|Malayalam|Mlym|
|Nepali|nep|
|Punjabi_Gurmukhī|Guru|
|Sanskrit|san|
|Sundanese|Sund|
|Thaana|Thaa|
</details>


<a name="Supported_Syllabaries"></a>
## Supported Syllabaries
<details><summary>Open to view all supported syllabaries</summary>

|Syllabary|ISO code|
|---|---|
|Avestan|Avst|
|Carian|Cari|
|Cherokee|Cher|
|Hiragana|Hira|
|Katakana|Kana|
|Lydian|Lydi|
</details>

<a name="Supported_Logographics"></a>
## Supported Logographics
<details><summary>Open to view all supported logographics</summary>

|Logographic|ISO code|
|---|---|
|Chinese_Simplified|Hans|
|Kanji|Hani|
</details>

<a name="Supported_Featurals"></a>
## Supported featural writing systems
<details><summary>Open to view all supported featurals</summary>

|Featural|ISO code|
|---|---|
|Hangul|Hang|
</details>


<a name="Design_Considerations"></a>
## Design Considerations / Limitations
Once delving deeper into the world of [writing systems](https://en.wikipedia.org/wiki/List_of_writing_systems), one is overwhelmed by the numerous difficulties that arise when organizing the various script types. This is particularly difficult when it comes to non-Latin scripts with their many variabilities and forms. Therefore, various design considerations were made to make Alphabetic as simple and usable as possible. 

- For languages that exhibit several variants of alphabets, the **more modern** or the **most frequently** encountered form was used. References to sources such as Omniglot, Wikipedia and Britannica were used for this purpose. 

- For Arabic scripts where the character form depends on its position, the so-called [isolated forms](https://www.arabacademy.com/the-different-forms-of-arabic-letters-and-how-they-come-together/) were used. 

- Multigraphs are considered as part of the scripts. However, if desired they can be [suppressed](#Usage). The same applies to [diacritical marks](https://en.wikipedia.org/wiki/Diacritic) (e.g., acute, breve, cédille, gravis, etc.). 

- The function ```is_abugida``` is **not** fully functional because not all vowel forms are integrated yet. 

- For so-called [non-bicameral](https://www.liquidbubble.co.uk/blog/the-comprehensive-guide-to-typography-jargon-for-designers/) languages such as *Hebrew* or *Arabic*, where there is **no distinction between upper and lower case**, the respective filter ``` letter_case=``` argument is ignored and the entire alphabet is returned instead:

```python
ws.pretty_print(ws.by_language(ws.Language.Hebrew, letter_case=ws.LetterCase.Upper))
                                                   
# א ב ג ד ה ו ז ח ט י כ ך ל מ ם נ ן ס ע פ ף צ ץ ק ר ש ת

ws.pretty_print(ws.by_language(ws.Language.Arabic, letter_case=ws.LetterCase.Lower))

# ا ب ة ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي
```

## Contribution
If you like this project, you are welcome to support it, e.g. by testing it or providing additional languages (there is a **lot** to do with regard to the [remaining languages](https://www.omniglot.com/writing/languages.htm)). Feel free to fork the repository and create a pull request to suggest and collaborate on changes.

## Disclaimer
Although this project has been carried out with great care, no liability is accepted for the completeness and accuracy of all the underlying data. The use of Alphabetic for integration into production systems is at your own risk!

Furthermore, please note that this project is still in its initial phase. The code structure may therefore change over time.

## Citation
If you find this repository helpful, feel free to cite it in your paper or project: 
```bibtex
@software{Halvani_Constituent_Treelib:2024,
	author = {Halvani, Oren},
	title = {{Alphabetic - A Python module for retrieving script types of writing systems including alphabets, abjads, abugidas, syllabaries, logographs, featurals as well as Latin script codes}},
	doi = {https://doi.org/10.5281/zenodo.11580510},
	month = jun,	
	url = {https://github.com/Halvani/alphabetic},
	version = {0.0.5},
	year = {2024}
}
```

## License
The Alphabetic package is released under the Apache-2.0 license. See <a href="https://github.com/Halvani/alphabetic/blob/main/LICENSE">LICENSE</a> for further details.


## Last Remarks
As is usual with open source projects, we developers do not earn any money with what we do, but are primarily interested in giving something back to the community with fun, passion and joy. Nevertheless, we would be very happy if you rewarded all the time that has gone into the project with just a small star 🤗