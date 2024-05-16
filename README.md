<div align="center">
  <p><a href="#"><img src="https://raw.githubusercontent.com/Halvani/alphabetic/main/assets/images/logo.jpg" alt="Alphabetic logo"/></a></p>
</div>

# Alphabetic
A lightweight Python module for querying language alphabets, codes, syllabaries and logographics

## Description
Alphabetic is a small project that was born out of the need to find out the alphabet of several languages for a private NLP project. Determining the alphabet of a language is important for various NLP tasks (e.g., for classifying the language of a given text or for normalizing it by removing noisy/random strings). 

The idea is simple: given the name of the [desired language](#Supported_Languages), [syllabary](#Supported_Syllabaries)  [logographic](#Supported_Logographics), Alphabetic first translates the language internally into a respective ISO-code (either [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php) or [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924)) and then returns the corresponding script. 

## Installation
The easiest way to install Alphabetic is to use pip, where you can choose between (1) the PyPI repository and (2) this repository. 

- (1) ```pip install alphabetic```
- (2) ```pip install git+https://github.com/Halvani/alphabetic.git```

The latter will pull and install the latest commit from this repository as well as the required Python dependencies. 

## Usage
A simple lookup of a language's alphabet can be performed as follows:
```python
from alphabetic import (Language, WritingSystem)

print(*WritingSystem.by_language(Language.Greek))

# Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω
```

Depending on the [selected language](#Supported_Languages), the output of  ```by_language``` can be either a list containing the accociated alphabet or a dictionary of accociated writing system types (e.g., Syllabary or Logographic). This is a [design consideration](#Design_Considerations) that results from the fact that certain languages such as [Japanese have no alphabet but instead three writing systems](https://www.busuu.com/en/japanese/alphabet). So in this case the output would look like this: 
```python
from alphabetic import (Language, WritingSystem)

print(WritingSystem.by_language(Language.Japanese))

# {'Hiragana': ['あ', 'い', ...], 'Katakana': ['ア', 'イ', 'ウ', ...], 'Kanji': ['一', '丁', '七', ...]
```

In cases where the given language has an alphabet, the result can be filtered in terms of: 
- **Letter casing**:
```python
from alphabetic import (Language, LetterCase, WritingSystem)

# print(*WritingSystem.by_language(Language.Bosnian))

# Ђ Ј Љ Њ Ћ Џ А Б В Г Д Е Ж З И К Л М Н О П Р С Т У Ф Х Ц Ч Ш а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ђ ј љ њ ћ џ

print(*WritingSystem.by_language(Language.Bosnian, letter_case=LetterCase.Lower))

# а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ђ ј љ њ ћ џ
```

- **Diphthongs**:
```python

# print(*WritingSystem.by_language(Language.Albanian))

# A B C Ç D Dh E Ë F G Gj H I J K L Ll M N Nj O P Q R Rr S Sh T Th U V X Xh Y Z Zh a b c ç d dh e ë f g gj h i j k l ll m n nj o p q r rr s sh t th u v x xh y z zh

print(*WritingSystem.by_language(Language.Albanian, strip_diphthongs=True))

# A B C Ç D E Ë F G H I J K L M N O P Q R S T U V X Y Z a b c ç d e ë f g h i j k l m n o p q r s t u v x y z
```

- **Diacritics**
```python
print(*WritingSystem.by_language(Language.Czech, strip_diacritics=True))

# A B C C h D E F G H I J K L M N O P Q R S T U V W X Y Z a b c c h d e f g h i j k l m n o p q r s t u v w x y z
```
For certain languages such as Chinese (simplified), which have a language code but no alphabet, a fallback strategy is used which maps the ISO 639-2 language code to an ISO 15924 code (as an example here: "chi" --> "Hans"). As a user, you do not have to handle this manually, but simply call up the language as it is:

```python
print(*WritingSystem.by_language(Language.Chinese_Simplified))

# 㑇 㑊 㕮 㘎 㙍 㙘 㙦 㛃 㛚 㛹 㟃 㠇 㠓 㤘 㥄 㧐 ...
```

## Features
- Currently [128 languages](#Supported_Languages) and the corresponding alphabets are supported, with more to follow over time.

- Beside alphabets, other writing systems / scripts are supported (e.g., [abugidas](https://en.wikipedia.org/wiki/Abugida), [syllabaries](https://en.wikipedia.org/wiki/Syllabary), [logographics](https://en.wikipedia.org/wiki/Logogram) and Latin script representations (e.g., [Morse](https://en.wikipedia.org/wiki/Morse_code) or [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet)))

- At the heart of Alphabetic are several [json files](https://github.com/Halvani/alphabetic/blob/main/alphabetic/data) that can be used independently of the respective programming language or application




<a name="Supported_Languages"></a>
## Supported languages
<details><summary>Open to view all supported languages</summary>

|Language|ISO 639-2 code|
|---|---|
|Abkhazian|abk|
|Afar|aar|
|Afrikaans|afr|
|Albanian|sqi|
|Amharic|amh|
|Arabic|ara|
|Armenian|arm|
|Assamese|asm|
|Avar|ava|
|Avestan|ave|
|Bambara|bam|
|Bashkir|bak|
|Basque|baq|
|Belarusian|bel|
|Bislama|bis|
|Boko|bqc|
|Bosnian|bos|
|Breton|bre|
|Bulgarian|bul|
|Buryat|bua|
|Catalan|cat|
|Chamorro|cha|
|Chechen|che|
|Cherokee|chr|
|Chichewa|nya|
|Chinese|chi|
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
|Gaelic|gla|
|Georgian|kat|
|German|deu|
|Greek|gre|
|Guarani|grn|
|Haitian|hat|
|Hausa|hau|
|Hawaiian|haw|
|Hebrew|heb|
|Herero|her|
|Hindi|hin|
|Icelandic|isl|
|Igbo|ibo|
|Indonesian|ind|
|Italian|ita|
|Japanese|jpn|
|Javanese|jav|
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
|Pashto|pus|
|Persian|per|
|Polish|pol|
|Portuguese|por|
|Punjabi|pan|
|Quechua|que|
|Rohingya|rhg|
|Russian|rus|
|Samoan|smo|
|Sango|sag|
|Sanskrit|san|
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

<a name="Supported_Syllabaries"></a>
## Supported syllabaries
<details><summary>Open to view all supported syllabaries</summary>

|Syllabary|15924 code|
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

|Logographic|15924 code|
|---|---|
|Chinese_Simplified|Hans|
|Kanji|Hani|
</details>

<a name="Design_Considerations"></a>
## Design considerations
Once delving deeper into the world of [writing systems](https://en.wikipedia.org/wiki/List_of_writing_systems), one is overwhelmed by the numerous difficulties that arise when organizing the various alphabets, syllabaries and logographies. This is particularly difficult when it comes to non-Latin scripts with their many variabilities and forms. Therefore, various design considerations were made to make "Alphabetic" as simple and usable as possible. 

- For languages that exhibit several variants of alphabets, the more modern or the most frequently encountered form was used. References to sources such as Omniglot, Wikipedia and Britannica were used for this purpose. 

- For Arbaic scripts where the character form depends on its position, the so-called [isolated forms](https://www.arabacademy.com/the-different-forms-of-arabic-letters-and-how-they-come-together/) were used. 

- For languages that contain diphthongs, these were integrated into the alphabets. These can be suppressed if required. The same applies to [diacritical marks](https://en.wikipedia.org/wiki/Diacritic) (e.g., acute, breve, cédille, gravis, etc.). 

- For so-called [non-bicameral](https://www.liquidbubble.co.uk/blog/the-comprehensive-guide-to-typography-jargon-for-designers/) such as *Hebrew* and *Arabic*, where there is **no distinction between upper and lower case**, the respective filter ``` letter_case=``` argument is ignored and the entire alphabet is returned instead:

```python
from alphabetic import (Language, LetterCase, WritingSystem)

print(*WritingSystem.by_language(Language.Hebrew, letter_case=LetterCase.Upper))

# א ב ג ד ה ו ז ח ט י כ ך ל מ ם נ ן ס ע פ ף צ ץ ק ר ש ת

print(*WritingSystem.by_language(Language.Arabic, letter_case=LetterCase.Lower))

# ا ب ة ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي
```

## Contribution
If you like this project, you are welcome to support it, e.g. by providing additional languages  (there is a lot to do with regard to [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php)). Feel free to fork the repository and create a pull request to suggest and collaborate on changes.

## Disclaimer
Although this project has been carried out with great care, we accept no liability for the completeness and accuracy of all data. The use of this data for integration into production systems is at your own risk.

Please also note that this project is still in the initial phase. Therefore, the code structure may change over time.

## Last remarks
As is usual with open source projects, we developers do not earn any money with what we do, but are primarily interested in giving something back to the community with fun, passion and joy. Nevertheless, we would be very happy if you rewarded all the time that has gone into the project with just a small star 🤗