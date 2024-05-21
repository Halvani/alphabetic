<div align="center">
  <p><a href="#"><img src="https://raw.githubusercontent.com/Halvani/alphabetic/main/assets/images/logo.jpg" alt="Alphabetic logo"/></a></p>
</div>

# Alphabetic
A Python module for querying writing systems of languages, including alphabets, abjads, abugidas, syllabaries, logographics as well as Latin script codes.

## Description / Background
Alphabetic is a small project that was born out of the need to find out the alphabet of several languages for a private NLP project. Determining the alphabet (as well as other script types) of a language is important for various NLP tasks (e.g., for classifying the language of a given text or for normalizing it by removing noisy/random strings). 

The basic idea is simple: given the name of the [desired language](#Supported_Languages), Alphabetic first translates it internally into a respective ISO-code (either [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php) or [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924)) and then returns the accociated script, which might be an [alphabet](https://en.wikipedia.org/wiki/Alphabet), [abjad](https://en.wikipedia.org/wiki/Abjad), [abugida](https://en.wikipedia.org/wiki/Abugida), [syllabary](https://en.wikipedia.org/wiki/Syllabary) or [logographic](https://en.wikipedia.org/wiki/Logogram). 

One might ask why such a distinction between "scripts" is necessary, and the answer is that the [writing systems](https://en.wikipedia.org/wiki/Writing_system) of languages differ depending on many factors. In Chinese, for example, [there is no alphabet](https://www.berlitz.com/blog/chinese-alphabet). This is confusing, as the following Python function, for example, suggests exactly that: 

```python
print("伏伐休众优伙".isalpha())

# True
```
The (linguistically) correct answer, however, should be **False** given the fact that the [Chinese writing system is logographic](https://en.wikipedia.org/wiki/Simplified_Chinese_characters). On the other hand, the following query:
```python
print("अमित".isalpha())
       
# False
```
is correct because Hindi is written in the Devanagari script, which is [not considered an alphabet but an abugida](https://en.wikipedia.org/wiki/Devanagari). To counteract such design decisions, which are described in the section *4.10 "Letters, Alphabetic, and Ideographic"* of the [Unicode Standard](https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf), Alphabetic can be used. This and other use cases are described [here](#Usage). 

## Installation
The easiest way to install Alphabetic is to use pip, where you can choose between (1) the PyPI repository and (2) this repository. 

- (1) ```pip install alphabetic```
- (2) ```pip install git+https://github.com/Halvani/alphabetic.git```

The latter will pull and install the latest commit from this repository as well as the required Python dependencies. 

<a name="Usage"></a>
## Usage
A simple lookup of a language's alphabet can be performed as follows:
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
In case that the resulting script type represents an alphabet, the result can be filtered in terms of: 
- **Letter casing**:
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

## Features
- Currently [140 languages](#Supported_Languages) and the corresponding scripts are supported, with more to follow over time.

- In total, Alphabet covers 6 script types: [abjads](https://en.wikipedia.org/wiki/Abjad), [abugidas](https://en.wikipedia.org/wiki/Abugida), [alphabets](https://en.wikipedia.org/wiki/Alphabet), [syllabaries](https://en.wikipedia.org/wiki/Syllabary), [logographics](https://en.wikipedia.org/wiki/Logogram) as well as [featural writing system](https://en.wikipedia.org/wiki/Featural_writing_system). 

- Besides, (true) writing systems, Alphabet also offers Latin script representations (e.g., [Morse](https://en.wikipedia.org/wiki/Morse_code) or [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet)).

- At the heart of Alphabetic are several [json files](https://github.com/Halvani/alphabetic/blob/main/alphabetic/data) that can be used independently of the respective programming language or application.


<a name="Supported_Languages"></a>
## Supported languages
<details><summary>Open to view all supported languages</summary>

|Language|ISO 639-2 code|
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
|Corsican|cos|
|Cree|cre|
|Croatian|hrv|
|Czech|ces|
|Danish|dan|
|Dungan|dng|
|Dutch|nld|
|Dzongkha|dzo|
|English|eng|
|Esperanto|epo|
|Estonian|est|
|Ewe|ewe|
|Faroese|fao|
|Fijian|fij|
|Finnish|fin|
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
|Punjabi|pan|
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
|Volapük|vol|
|Welsh|wel|
|Wolof|wol|
|Yakut|sah|
|Yiddish|yid|
|Zulu|zul|
</details>


<a name="Supported_Abjads"></a>
## Supported abjads
<details><summary>Open to view all supported abjads</summary>

|Abjad|ISO code|
|---|---|
|Arabic|Arab|
|Balochi|bal|
|Hebrew|Hebr|
|Hebrew_Samaritan|Samr|
|Parthian|Prti|
|Phoenician|Phnx|
|Ugaritic|Ugar|
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
|Hindi|hin|
|Javanese|Java|
|Malayalam|Mlym|
|Sundanese|Sund|
|Thaana|Thaa|
</details>


<a name="Supported_Syllabaries"></a>
## Supported syllabaries
<details><summary>Open to view all supported syllabaries</summary>

|Syllabary|ISO code|
|---|---|
|Avestan|Avst|
|Carian|Cari|
|Cherokee|Cher|
|Ethiopic|Ethi|
|Hiragana|Hira|
|Katakana|Kana|
|Lydian|Lydi|
</details>

<a name="Supported_Logographics"></a>
## Supported logographics
<details><summary>Open to view all supported logographics</summary>

|Logographic|ISO code|
|---|---|
|Chinese_Simplified|Hans|
|Kanji|Hani|
</details>

<a name="Supported_Featurals"></a>
## Supported Featural writing systems
<details><summary>Open to view all supported featurals</summary>

|Featural|ISO code|
|---|---|
|Hangul|Hang|
</details>


<a name="Design_Considerations"></a>
## Design considerations
Once delving deeper into the world of [writing systems](https://en.wikipedia.org/wiki/List_of_writing_systems), one is overwhelmed by the numerous difficulties that arise when organizing the various alphabets, syllabaries and logographies. This is particularly difficult when it comes to non-Latin scripts with their many variabilities and forms. Therefore, various design considerations were made to make "Alphabetic" as simple and usable as possible. 

- For languages that exhibit several variants of alphabets, the more modern or the most frequently encountered form was used. References to sources such as Omniglot, Wikipedia and Britannica were used for this purpose. 

- For Arbaic scripts where the character form depends on its position, the so-called [isolated forms](https://www.arabacademy.com/the-different-forms-of-arabic-letters-and-how-they-come-together/) were used. 

- Multigraphs are considered as part of the scripts. However, if desired they can be [suppressed](#Usage). The same applies to [diacritical marks](https://en.wikipedia.org/wiki/Diacritic) (e.g., acute, breve, cédille, gravis, etc.). 

- In case of abugida-based scripts [dependent vowels](https://en.wikipedia.org/wiki/Khmer_script#Dependent_vowels) are not considered as part of the script for complexity resaons.   

- For so-called [non-bicameral](https://www.liquidbubble.co.uk/blog/the-comprehensive-guide-to-typography-jargon-for-designers/) languages such as *Hebrew* or *Arabic*, where there is **no distinction between upper and lower case**, the respective filter ``` letter_case=``` argument is ignored and the entire alphabet is returned instead:

```python
ws.pretty_print(ws.by_language(ws.Language.Hebrew, letter_case=ws.LetterCase.Upper))
                                                   
# א ב ג ד ה ו ז ח ט י כ ך ל מ ם נ ן ס ע פ ף צ ץ ק ר ש ת

ws.pretty_print(ws.by_language(ws.Language.Arabic, letter_case=ws.LetterCase.Lower))

# ا ب ة ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي
```

## Contribution
If you like this project, you are welcome to support it, e.g. by providing additional languages  (there is a **lot* to do with regard to the remaining languages listed under the [ISO 639-2 website](https://www.loc.gov/standards/iso639-2/php/code_list.php)). Feel free to fork the repository and create a pull request to suggest and collaborate on changes.

## Disclaimer
Although this project has been carried out with great care, no liability is accepted for the completeness and accuracy of all the underlying data. The use of Alphabetic for integration into production systems is at your own risk.

Please also note that this project is still in the initial phase. Therefore, the code structure may change over time.

## Last remarks
As is usual with open source projects, we developers do not earn any money with what we do, but are primarily interested in giving something back to the community with fun, passion and joy. Nevertheless, we would be very happy if you rewarded all the time that has gone into the project with just a small star 🤗