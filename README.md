# Alphabetic
A lightweight Python module for querying language alphabets, codes, syllabaries and logographics

# Description
Alphabetic is a small project that was born out of the need to find out the alphabet of several languages for a private NLP project. Determining the alphabet of a language is required for various NLP tasks, e.g. for classifying the language of a given text or for normalizing it (e.g., by removing noisy/random strings). 

The idea is simple: given the name of the desired language (e.g. *German*, *Serbian*, *Estonian*, etc.), Alphabetic first translates the language internally into an [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php) language code and then returns the corresponding alphabet. 

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

The output of  ```by_language``` is a simple list of utf8-strings. Depending on the selected language, the alphabet can be further restricted in terms of letter casing: 

```python
from alphabetic import Language, Alphabet, LetterCase 

print(*Alphabet.by_language(Language.Bosnian, letter_case=LetterCase.Lower))

# а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ђ ј љ њ ћ џ
```
However, for some languages (e.g. *Hebrew* or *Arabic*, which have no upper/lower case) such restrictions are not possible. Therefore, in such cases, the entire alphabet is returned...

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
print(*Alphabet.by_language(Language.Czech, only_true_alphabet=True))

# A B C C h D E F G H I J K L M N O P Q R S T U V W X Y Z a b c c h d e f g h i j k l m n o p q r s t u v w x y z
```

# Features
- Currently 72 languages are supported, with more to follow over time
- At the heart of Alphabetic is a [Json file](https://github.com/Halvani/alphabetic/blob/main/alphabetic/data/language_data.json) that can be used independently of the respective programming language or application
- Besides langauge alphabets, Alphabetic also provides codes (e.g., [Morse](https://en.wikipedia.org/wiki/Morse_code) or [NATO Phonetic Alphabet](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet)), [Syllabaries](https://en.wikipedia.org/wiki/Syllabary) and [Logographics](https://en.wikipedia.org/wiki/Logogram)


# Supported languages
<details><summary>Open to view all supported languages</summary>

|Language|ISO 639-2 code|
|---|---|
|Albanian|sqi|
|Arabic|ara|
|Bashkir|bak|
|Belarusian|bel|
|Boko|bqc|
|Bosnian|bos|
|Bulgarian|bul|
|Buryat|bua| 
|Catalan|cat|
|Chechen|che|
|Cherokee|chr| 
|Chukchi|ckt|
|Croatian|hrv|
|Czech|ces|
|Danish|dan|
|Dungan|dng|
|Dutch|nld|
|English|eng|
|Esperanto|epo|
|Estonian|est|
|Finnish|fin|
|French|fra|
|Georgian|kat|
|German|deu|
|Greek|gre|
|Hawaiian|haw|
|Hebrew|heb|
|Icelandic|isl|
|Indonesian|ind|
|Italian|ita|
|Kashubian|csb|
|Kazakh|kaz|
|Kirghiz / Kyrgyz|kir|
|Korean|kor|
|Kumyk|kum|
|Kurmanji|kmr|
|Latin|lat|
|Latvian|lav|
|Lezghian|lez|
|Lithuanian|lit|
|Macedonian|mkd|
|Malay|may|
|Maltese|mlt|
|Maori|mao|
|Mari|chm|
|Moldovan |rum|
|Mongolian|mon|
|Mru|mro|
|Nepali |nep|
|Norwegian |nor|
|Polish|pol|
|Portuguese|por|
|Rohingya |rhg|
|Romanian|rum|
|Russian|rus|
|Sanskrit|san|
|Serbian|srp|
|Slovak|slo|
|Slovenian / Slovene|slv|
|Somali|som|
|Sorani|ckb| 
|Spanish|spa|
|Sundanese|sun|
|Swedish|swe|
|Tajik |tgk|
|Tatar|tat|
|Turkish|tur|
|Turkmen|tuk|
|Ukrainian|ukr|
|Wolof|wol|
|Yakut|sah|
|Yiddish|yid|
|Zulu|zul|
</details>
<br>

# Contribution
If you like this project, you are welcome to support it, e.g. by providing additional languages  (there is a lot to do with regard to [ISO 639-2](https://www.loc.gov/standards/iso639-2/php/code_list.php)). Feel free to fork the repository and create a pull request to suggest and collaborate on changes.

# Last remarks
As is usual with open source projects, we developers do not earn any money with what we do, but are primarily interested in giving something back to the community with fun, passion and joy. Nevertheless, we would be very happy if you rewarded all the time that has gone into the project with just a small star 🤗 



