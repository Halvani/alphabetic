# Alphabetic
A lightweight Python module for querying language alphabets, codes, syllabaries and logographics

# Description
Alphabetic is a small project that was born out of the need to find out the alphabet of several languages for a private NLP project. Determining the alphabet of a language is required for various NLP tasks, e.g. for classifying the language of a given text or for normalizing it (e.g., by removing noisy/random strings). 

The idea is simple: given the name of the [desired language](#Supported_Languages), Alphabetic first translates the language internally into an [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php) language code and then returns the corresponding alphabet. 

# Installation
The easiest way to install Alphabetic is to use pip, where you can choose between (1) the PyPI repository and (2) this repository. 

- (1) ```pip install alphabetic```
- (2) ```pip install git+https://github.com/Halvani/alphabetic.git```

The latter will pull and install the latest commit from this repository as well as the required Python dependencies. 

# Usage
A simple lookup of a language's alphabet can be performed as follows:
```python
from alphabetic import Language, Alphabet

print(*Alphabet.by_language(Language.Greek))

# Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω
```

The output of  ```by_language``` is a list of utf8-strings. Depending on the [selected language](#Supported_Languages), the alphabet can be further restricted in terms of letter casing: 

```python
from alphabetic import Language, Alphabet, LetterCase 

print(*Alphabet.by_language(Language.Bosnian, letter_case=LetterCase.Lower))

# а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ђ ј љ њ ћ џ
```
Note that for some so-called [non-bicameral](https://www.liquidbubble.co.uk/blog/the-comprehensive-guide-to-typography-jargon-for-designers/) languages such as *Hebrew* or *Arabic*, which have **no** upper/lower case, such restrictions are not possible. Therefore, in such cases, the entire alphabet is returned:

```python
from alphabetic import Language, Alphabet, LetterCase 

print(*Alphabet.by_language(Language.Hebrew, letter_case=LetterCase.Lower))

# א ב ג ד ה ו ז ח ט י כ ך ל מ ם נ ן ס ע פ ף צ ץ ק ר ש ת

print(*Alphabet.by_language(Language.Arabic, letter_case=LetterCase.Lower))

# ا ب ة ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي
```

According to [Wikipedia](https://en.wikipedia.org/wiki/List_of_writing_systems#Syllabaries): 
"*A true alphabet contains separate letters (**not diacritic marks**) for both consonants and vowels.*" In order to strip out diacritics from a desired alphabet, you can restrict the output of ```by_language``` as follows:
```python
print(*Alphabet.by_language(Language.Czech, strip_diacritics=True))

# A B C C h D E F G H I J K L M N O P Q R S T U V W X Y Z a b c c h d e f g h i j k l m n o p q r s t u v w x y z
```

Moreover, you can strip out diphthongs that are present for several languages:
```python

print(*Alphabet.by_language(Language.Albanian)

# Entire alphabet: A B C Ç D Dh E Ë F G Gj H I J K L Ll M N Nj O P Q R Rr S Sh T Th U V X Xh Y Z Zh a b c ç d dh e ë f g gj h i j k l ll m n nj o p q r rr s sh t th u v x xh y z zh

print(*Alphabet.by_language(Language.Albanian, strip_diphthongs=True))

# A B C Ç D E Ë F G H I J K L M N O P Q R S T U V X Y Z a b c ç d e ë f g h i j k l m n o p q r s t u v x y z
```

# Features
- Currently 117 languages are supported, with more to follow over time
- At the heart of Alphabetic is a [json file](https://github.com/Halvani/alphabetic/blob/main/alphabetic/data/language_data.json) that can be used independently of the respective programming language or application
- Besides langauge alphabets, Alphabetic also provides codes (e.g., [Morse](https://en.wikipedia.org/wiki/Morse_code) or [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet)), [syllabaries](https://en.wikipedia.org/wiki/Syllabary) and [logographics](https://en.wikipedia.org/wiki/Logogram)


<a name="Supported_Languages"></a>
# Supported languages
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
|Chukchi|ckt|
|Chuvash|chv|
|Corsican|cos|
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
|Javanese|jav|
|Kabardian|kbd|
|Kashubian|csb|
|Kazakh|kaz|
|Kirghiz|kir|
|Komi|kpv|
|Korean|kor|
|Kumyk|kum|
|Kurmanji|kmr|
|Latin|lat|
|Latvian|lav|
|Lezghian|lez|
|Lithuanian|lit|
|Luganda|lug|
|Macedonian|mkd|
|Malay|may|
|Maltese|mlt|
|Maori|mao|
|Mari|chm|
|Moksha|mdf|
|Moldovan|rum|
|Mongolian|mon|
|Mru|mro|
|Nepali|nep|
|Norwegian|nor|
|Occitan|oci|
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

# Contribution
If you like this project, you are welcome to support it, e.g. by providing additional languages  (there is a lot to do with regard to [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php)). Feel free to fork the repository and create a pull request to suggest and collaborate on changes.

# Last remarks
As is usual with open source projects, we developers do not earn any money with what we do, but are primarily interested in giving something back to the community with fun, passion and joy. Nevertheless, we would be very happy if you rewarded all the time that has gone into the project with just a small star 🤗 



