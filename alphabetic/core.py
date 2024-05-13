import dcl
import json
from pathlib import Path
from enum import Enum, auto

from .errors import *

# Notes: 
# -------------------------------
# ISO 639 is a standardized nomenclature used to classify languages. Each language is assigned a two-letter (set 1) and three-letter lowercase abbreviation (sets 2–5). 
# Alphabetic uses in almost all cases ISO 639-2 as a language code identifier. However, in cases where no ISO 639-2 fields were available (e.g., "Komi") the ISO 639-3 code was used instead.    
#
# Sources of alphabets --> https://www.omniglot.com/index.htm; https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes    
# Sources of language code listings --> https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes ; https://de.wikipedia.org/wiki/Kategorie:Alphabet
#
# Japanese --> Hiragana and Katakana are not letters. There is no alphabet in Japanese; the Kana form a syllabary, not an alphabet.
# True alphabets: A true alphabet contains separate letters (not diacritic marks) for both consonants and vowels. --> https://en.wikipedia.org/wiki/List_of_writing_systems#Syllabaries
# Languages without casing distinction: Amharic, Arabic, Assamese, Azerbaijani, Brahui, Balinese, Baluchi, Batak, Baybayin, Bengali, Bilen, Burmese, Chinese, Georgian, Gujarati, Gurmukhi, Hebrew, Hindi, Japanese, Kannada, Kashmiri, Khmer, Korean, Kurdish, Central, Lao, Lontara, Malayalam, Middle Brahmi, Odia, Pashto, Persian, Punjabi, Sindhi, Sinhala, Sundanese, Sylheti, Tamil, Telugu, Thai, Tibetan, Tigre, Tigrinya, Tirhuta, Urdu, Uyghur, Yiddish   --> https://www.quora.com/Which-languages-have-no-capitalized-letter
# Moldovan and Romanian share the same alphabet and language code ("rum") --> https://en.wikipedia.org/wiki/Moldovan_language
# Hindi: Hindi is written in the Devanagari script --> https://en.wikipedia.org/wiki/Devanagari
# Sanskrit: Currently, Devanagari serves as its writing system --> https://www.easyhindityping.com/sanskrit-alphabet
# Diacritical marks: A number of languages (e.g., French, German, Spanish, Italian, Portuguese, Polish, Czech, Swedish, etc.) make use of diacritics. --> https://entnemdept.ufl.edu/frank/kiss/kiss3.htm
# Sundanese: These days Sundanese is normally written with the Latin alphabet, however the Sundanese script is still used to some extent. 
# Zulu: Additional phonemes in Zulu are written using sequences of multiple letters. However, it is not clear if they count as alphabetic letters too.  -->  https://en.wikipedia.org/wiki/Zulu_language
# Basque: Basque is written using the Latin script including ⟨ñ⟩ and sometimes ⟨ç⟩ and ⟨ü⟩. Basque does not use ⟨c, q, v, w, y⟩ for native words, but the Basque alphabet (established by Euskaltzaindia) does include them for loanwords --> https://en.wikipedia.org/wiki/Basque_language#Writing_system
#
# Clarify --> Hawar (Language?):   ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "Ç", "Ê", "Î", "Û", "ç", "ê", "î", "û", "Ş", "ş"], # https://en.wikipedia.org/wiki/Kurdish_alphabets
# Clarify --> Mahajani (Language?): ["𑅐", "𑅑", "𑅒", "𑅓", "𑅔", "𑅕", "𑅖", "𑅗", "𑅘", "𑅙", "𑅚", "𑅛", "𑅜", "𑅝", "𑅞", "𑅟", "𑅠", "𑅡", "𑅢", "𑅣", "𑅤", "𑅥", "𑅦", "𑅧", "𑅨", "𑅩", "𑅪", "𑅫", "𑅬", "𑅭", "𑅮", "𑅯", "𑅰", "𑅱", "𑅲"],  What is the language code? --> https://en.wikipedia.org/wiki/Mahajani 


def __load_json_content__(json_filename: str, 
                          enum_class: Enum,
                          key_name: str,
                          err_msg_enum_class: str):
            
    if not Path(json_filename).exists():
        err_msg = f"Internal json file: [{json_filename}] could not be found. This file contains all supported {err_msg_enum_class}."
        raise FileNotFoundError(err_msg)
    
    json_data = Path(json_filename).read_text(encoding="utf8")
    _dict = json.loads(json_data)
    iso_code = enum_class.value[0]

    return _dict[iso_code][key_name] 


class Language(Enum):
    Abkhazian = "abk",
    Afar = "aar",
    Afrikaans = "afr",
    Albanian = "sqi",
    Amharic = "amh",
    Arabic = "ara",
    Armenian = "arm",
    Assamese = "asm",
    Avar = "ava",
    Avestan = "ave",
    Bambara = "bam",
    Bashkir = "bak",
    Basque = "baq",
    Belarusian = "bel",
    Bislama = "bis",
    Boko = "bqc",
    Bosnian = "bos",
    Breton = "bre",
    Bulgarian = "bul",
    Buryat = "bua",
    Catalan = "cat",
    Chamorro = "cha",
    Chechen = "che",
    Cherokee = "chr",
    Chichewa = "nya",
    Chukchi = "ckt",
    Chuvash = "chv",
    Corsican = "cos",
    Croatian = "hrv",
    Czech = "ces",
    Danish = "dan",
    Dungan = "dng",
    Dutch = "nld",
    Dzongkha = "dzo",
    English = "eng",
    Esperanto = "epo",
    Estonian = "est",
    Ewe = "ewe",
    Faroese = "fao",
    Fijian = "fij",
    Finnish = "fin",
    French = "fra",
    Gaelic = "gla",
    Georgian = "kat",
    German = "deu",
    Greek = "gre",
    Guarani = "grn",
    Haitian = "hat",
    Hausa = "hau",
    Hawaiian = "haw",
    Hebrew = "heb",
    Herero = "her",
    Hindi = "hin",
    Icelandic = "isl",
    Igbo = "ibo",
    Indonesian = "ind",
    Italian = "ita",
    Javanese = "jav",
    Kabardian = "kbd",
    Kashubian = "csb",
    Kazakh = "kaz",
    Kirghiz = "kir",
    Komi = "kpv",
    Korean = "kor",
    Kumyk = "kum",
    Kurmanji = "kmr",
    Latin = "lat",
    Latvian = "lav",
    Lezghian = "lez",
    Lithuanian = "lit",
    Luganda = "lug",
    Macedonian = "mkd",
    Malay = "may",
    Maltese = "mlt",
    Maori = "mao",
    Mari = "chm",
    Moksha = "mdf",
    Moldovan = "rum",
    Mongolian = "mon",
    Mru = "mro",
    Nepali = "nep",
    Norwegian = "nor",
    Occitan = "oci",
    Pashto = "pus",
    Persian = "per",
    Polish = "pol",
    Portuguese = "por",
    Punjabi = "pan",
    Quechua = "que",
    Rohingya = "rhg",
    Russian = "rus",
    Samoan = "smo",
    Sango = "sag",
    Sanskrit = "san",
    Serbian = "srp",
    Slovak = "slo",
    Slovenian = "slv",
    Somali = "som",
    Sorani = "ckb",
    Spanish = "spa",
    Sundanese = "sun",
    Swedish = "swe",
    Tajik = "tgk",
    Tatar = "tat",
    Turkish = "tur",
    Turkmen = "tuk",
    Tuvan = "tyv",
    Twi = "twi",
    Ukrainian = "ukr",
    Uzbek = "uzb",
    Venda = "ven",
    Volapük = "vol",
    Welsh = "wel",
    Wolof = "wol",
    Yakut = "sah",
    Yiddish = "yid",
    Zulu = "zul",

    
class LetterCase(Enum):
    Lower = auto(),
    Upper = auto(),
    Both = auto()

class Code(Enum):
    Morse = auto(),
    NATO_Phonetic_Alphabet = auto(),     

class Syllabary(Enum):
    Hiragana = "Hira",
    Cherokee = "Cher",
    Katakana = "Kana",

class Logographic(Enum):
    Kanji = "Hani",

class Script:
    @staticmethod
    def by_syllabary(syllabary: Syllabary, json_filename: str = r"alphabetic/data/syllabary_data.json") -> list[str]:
         return __load_json_content__(json_filename, 
                                      syllabary,
                                      key_name = "script",
                                      err_msg_enum_class = "syllabaries")
    
    @staticmethod
    def by_logographic(logographic: Logographic, json_filename: str = r"alphabetic/data/logographic_data.json") -> list[str]:
        return __load_json_content__(json_filename,
                                     logographic,
                                     key_name = "script",
                                     err_msg_enum_class = "logographics")       

class Alphabet:
    @staticmethod
    def update_lang_json_file(langcode: str, 
                              alphabet: list[str], 
                              json_filename: str = r"alphabetic/data/alphabet_data.json") -> None:
        
        json_data = Path(json_filename).read_text(encoding="utf8")
        alphabet_dict = json.loads(json_data)

        alphabet_dict[langcode] = {"alphabet": alphabet}
        Path(json_filename).write_text(json.dumps(alphabet_dict), encoding="utf8")

        created_dict = json.loads(Path(json_filename).read_text(encoding="utf8"))

        if langcode in created_dict:
            lang_dict = dict([(e.value[0], e.name) for e in Language])
            print(f"✅ Updated json-file successfully!\nLanguage: {lang_dict[langcode]}; "
                  f"Language code: {langcode}; Alphabet size: {len(created_dict[langcode]["alphabet"])} (characters).")    
        else:
            print("❌ Something went wrong! Specified json file could not be written.")  


    @staticmethod
    def provides_letter_cases(alphabet: list[str]) -> bool:
        return True if len([c for c in alphabet if c.isupper() or c.islower()]) > 0 else False 

    @staticmethod
    def extract_diacritics(alphabet: list[str]) -> list[str]:
        extracted_diacritics = dcl.get_diacritics("".join(alphabet) )
        return [c.character for _, c in extracted_diacritics.items()]
    
    @staticmethod
    def extract_diphthongs(alphabet: list[str]) -> list[str]:
        return [c for c in alphabet  if len(c) == 2]

    @staticmethod
    def by_code(code: Code) -> list[tuple[str,str]]:
        alphabet_dict = {
            Code.Morse : [("A", "▄ ▄▄▄"), ("B", "▄▄▄ ▄ ▄ ▄"), ("C", "▄▄▄ ▄ ▄▄▄ ▄"), ("D", "▄▄▄ ▄ ▄"), ("E", "▄"), ("F", "▄ ▄ ▄▄▄ ▄"), ("G", "▄▄▄ ▄▄▄ ▄"), ("H", "▄ ▄ ▄ ▄"), ("I", "▄ ▄"), ("J", "▄ ▄▄▄ ▄▄▄ ▄▄▄"), ("K", "▄▄▄ ▄ ▄▄▄"), ("L", "▄ ▄▄▄ ▄ ▄"), ("M", "▄▄▄ ▄▄▄"), ("N", "▄▄▄ ▄"), ("O", "▄▄▄ ▄▄▄ ▄▄▄"), ("P", "▄ ▄▄▄ ▄▄▄ ▄"), ("Q", "▄▄▄ ▄▄▄ ▄ ▄▄▄"), ("R", "▄ ▄▄▄ ▄"), ("S", "▄ ▄ ▄"), ("T", "▄▄▄"), ("U", "▄ ▄ ▄▄▄"), ("V", "▄ ▄ ▄ ▄▄▄"), ("W", "▄ ▄▄▄ ▄▄▄"), ("X", "▄▄▄ ▄ ▄ ▄▄▄"), ("Y", "▄▄▄ ▄ ▄▄▄ ▄▄▄"), ("Z", "▄▄▄ ▄▄▄ ▄ ▄")], 
            Code.NATO_Phonetic_Alphabet : [("A", "Alfa"), ("B", "Bravo"), ("C", "Charlie"), ("D", "Delta"), ("E", "Echo"), ("F", "Foxtrot"), ("G", "Golf"), ("H", "Hotel"), ("I", "India"), ("J", "Juliett"), ("K", "Kilo"), ("L", "Lima"), ("M", "Mike"), ("N", "November"), ("O", "Oscar"), ("P", "Papa"), ("Q", "Quebec"), ("R", "Romeo"), ("S", "Sierra"), ("T", "Tango"), ("U", "Uniform"), ("V", "Victor"), ("W", "Whiskey"), ("X", "Xray"), ("Y", "Yankee"), ("Z", "Zulu")]
        }
        return alphabet_dict[code]


    @staticmethod
    def by_language(language: Language, 
                    letter_case: LetterCase = LetterCase.Both,
                    strip_diacritics: bool = False,
                    strip_diphthongs: bool = False,
                    json_filename=r"alphabetic/data/alphabet_data.json") -> str:                
        
        alphabet = __load_json_content__(json_filename,
                                         language,
                                         key_name = "alphabet",
                                         err_msg_enum_class = "alphabets")         
        
        if strip_diacritics:
            diacritics = set(Alphabet.extract_diacritics(alphabet))
            alphabet = [c for c in alphabet if c not in diacritics]

        if strip_diphthongs:
            diphthongs = Alphabet.extract_diphthongs(alphabet)
            alphabet = [c for c in alphabet if c not in diphthongs]

        if letter_case == LetterCase.Both:
            return alphabet
        
        elif letter_case == LetterCase.Lower:
            if Alphabet.provides_letter_cases(alphabet):
                return [c for c in alphabet if c.islower()]
            else:
                return alphabet
            
        elif letter_case == LetterCase.Upper:
            if Alphabet.provides_letter_cases(alphabet):
                return [c for c in alphabet if c.isupper()]
            else:
                return alphabet