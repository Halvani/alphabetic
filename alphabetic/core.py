import dcl
import json
from pathlib import Path
from enum import Enum, auto
from .errors import *

# Notes: 
# -------------------------------
# The exact relationship between writing systems and languages can be complex. 
# A single language (e.g. Hindustani) can have multiple writing systems, and a writing system can also represent multiple languages. --> https://en.wikipedia.org/wiki/Writing_system

# ISO 639 is a standardized nomenclature used to classify languages. Each language is assigned a two-letter (set 1) and three-letter lowercase abbreviation (sets 2–5). 
# Alphabetic uses in almost all cases ISO 639-2 as a language code identifier. However, in cases where no ISO 639-2 fields were available (e.g., "Komi") the ISO 639-3 code was used instead.    
#
# Sources of alphabets --> https://www.omniglot.com/index.htm; https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes    
# Sources of language code listings --> https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes ; https://de.wikipedia.org/wiki/Kategorie:Alphabet
#
# True alphabets: A true alphabet contains separate letters (not diacritic marks) for both consonants and vowels. --> https://en.wikipedia.org/wiki/List_of_writing_systems#Syllabaries
# Languages without casing distinction: Amharic, Arabic, Assamese, Azerbaijani, Brahui, Balinese, Baluchi, Batak, Baybayin, Bengali, Bilen, Burmese, Chinese, Georgian, Gujarati, Gurmukhi, Hebrew, Hindi, Japanese, Kannada, Kashmiri, Khmer, Korean, Kurdish, Central, Lao, Lontara, Malayalam, Middle Brahmi, Odia, Pashto, Persian, Punjabi, Sindhi, Sinhala, Sundanese, Sylheti, Tamil, Telugu, Thai, Tibetan, Tigre, Tigrinya, Tirhuta, Urdu, Uyghur, Yiddish   --> https://www.quora.com/Which-languages-have-no-capitalized-letter
# Diacritical marks: A number of languages (e.g., French, German, Spanish, Italian, Portuguese, Polish, Czech, Swedish, etc.) make use of diacritics. --> https://entnemdept.ufl.edu/frank/kiss/kiss3.htm
#
# Cree: This language is considered to be a Syllabary according to: https://en.wikipedia.org/wiki/Cree_(language)#Writing 
# However, no ISO-15924 identifier can be found for it under: https://en.wikipedia.org/wiki/ISO_15924 Hencee, it is treated here as an alphabet.
#
# Japanese: There is no alphabet in Japanese. In fact, there are three writing systems called Hiragana, Katakana and Kanji. Katakana and Hiragana constitute syllabaries; 
# Katakana are primarily used to write foreign words, plant and animal names, and for emphasis. --> https://en.wikipedia.org/wiki/Japanese_language#Writing_system
#
# Chinese: According to Britannica, Chinese represents a logographic writing system -->  https://www.britannica.com/topic/Chinese-writing
# 
# Korean: Korean alphabet's (Hangul) has been described as a syllabic alphabet as it combines the features of alphabetic and syllabic writing systems. --> https://en.wikipedia.org/wiki/Korean_language#Writing_system
#
# Moldovan and Romanian share the same alphabet and language code ("rum") --> https://en.wikipedia.org/wiki/Moldovan_language
#
# Hindi: Hindi is written in the Devanagari script --> https://en.wikipedia.org/wiki/Devanagari
#
# Sanskrit: Currently, Devanagari serves as its writing system --> https://www.easyhindityping.com/sanskrit-alphabet
#
# Sundanese: These days Sundanese is normally written with the Latin alphabet, however the Sundanese script is still used to some extent. 
#
# Zulu: Additional phonemes in Zulu are written using sequences of multiple letters. However, it is not clear if they count as alphabetic letters too.  -->  https://en.wikipedia.org/wiki/Zulu_language
#
# Basque: Basque is written using the Latin script including ⟨ñ⟩ and sometimes ⟨ç⟩ and ⟨ü⟩. Basque does not use ⟨c, q, v, w, y⟩ for native words, but the Basque alphabet (established by Euskaltzaindia) does include them for loanwords --> https://en.wikipedia.org/wiki/Basque_language#Writing_system
#
# Clarify --> Hawar (Language?):   ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "Ç", "Ê", "Î", "Û", "ç", "ê", "î", "û", "Ş", "ş"], # https://en.wikipedia.org/wiki/Kurdish_alphabets
# Clarify --> Mahajani (Language?): ["𑅐", "𑅑", "𑅒", "𑅓", "𑅔", "𑅕", "𑅖", "𑅗", "𑅘", "𑅙", "𑅚", "𑅛", "𑅜", "𑅝", "𑅞", "𑅟", "𑅠", "𑅡", "𑅢", "𑅣", "𑅤", "𑅥", "𑅦", "𑅧", "𑅨", "𑅩", "𑅪", "𑅫", "𑅬", "𑅭", "𑅮", "𑅯", "𑅰", "𑅱", "𑅲"],  What is the language code? --> https://en.wikipedia.org/wiki/Mahajani 


    # chr
    # chi
    # jpn

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
    Chinese = "chi",
    Chukchi = "ckt",
    Chuvash = "chv",
    Corsican = "cos",
    Cree = "cre",
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
    Japanese = "jpn",
    Javanese = "jav",
    Kabardian = "kbd",
    Kanuri = "kau",
    Kashubian = "csb",
    Kazakh = "kaz",
    Kinyarwanda = "kin",
    Kirghiz = "kir",
    Komi = "kpv",
    Korean = "kor",
    Kumyk = "kum",
    Kurmanji = "kmr",
    Latin = "lat",
    Latvian = "lav",
    Lezghian = "lez",
    Lingala = "lin",
    Lithuanian = "lit",
    Luganda = "lug",
    Macedonian = "mkd",
    Malagasy = "mlg",
    Malay = "may",
    Malayalam = "mal",
    Maltese = "mlt",
    Manx = "glv",
    Maori = "mao",
    Mari = "chm",
    Marshallese = "mah",
    Moksha = "mdf",
    Moldovan = "rum",
    Mongolian = "mon",
    Mru = "mro",
    Nepali = "nep",
    Norwegian = "nor",
    Occitan = "oci",
    Oromo = "orm",
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


class JsonFile(Enum):
    LatinScriptCode = r"alphabetic/data/latin_script_code.json",
    Alphabet = r"alphabetic/data/alphabet.json",
    Abugida = r"alphabetic/data/abugida.json",
    Syllabary = r"alphabetic/data/syllabary.json",
    Logographic = r"alphabetic/data/logographic.json",

class LetterCase(Enum):
    Lower = auto(),
    Upper = auto(),
    Both = auto()

class LatinScriptCode(Enum):
    Morse = auto(),
    NATO_Phonetic_Alphabet = auto(),     

# Values represent ISO-15924 identifiers 
class Syllabary(Enum):
    Avestan = "Avst",
    Ethiopic = "Ethi",
    Carian = "Cari",
    Lydian = "Lydi",
    Hiragana = "Hira",
    Cherokee = "Cher",
    Katakana = "Kana",

# Values represent ISO-15924 identifiers
class Logographic(Enum):    
    Kanji = "Hani",
    Chinese_Simplified = "Hans",

# Values represent ISO-15924 identifiers
class Abugida(Enum):
    Thaana = "Thaa",



class JsonUtils:
    @staticmethod
    def load_dict_from_jsonfile(json_filename: JsonFile, err_msg_enum_class: str):
        json_filename = json_filename.value[0]
        if not Path(json_filename).exists():
            err_msg = f"Internal json file: [{json_filename}] could not be found. This file contains all supported {err_msg_enum_class}."
            raise FileNotFoundError(err_msg)
        
        json_data = Path(json_filename).read_text(encoding="utf8")
        return json.loads(json_data)
     
    @staticmethod
    def update_lang_json_file(langcode: str, alphabet: list[str]) -> None:
        json_filename = JsonFile.Alphabet.value[0]
        alphabet_dict = JsonUtils.load_dict_from_jsonfile(JsonFile.Alphabet, err_msg_enum_class = "alphabets")
        alphabet_dict[langcode] = {"alphabet": alphabet}
        Path(json_filename).write_text(json.dumps(alphabet_dict, ensure_ascii=False), encoding="utf8")
        created_dict = json.loads(Path(json_filename).read_text(encoding="utf8"))

        if langcode in created_dict:
            lang_dict = dict([(e.value[0], e.name) for e in Language])
            print(f"✅ Updated json-file successfully!\nLanguage: {lang_dict[langcode]}; "
                  f"Language code: {langcode}; Alphabet size: {len(created_dict[langcode]["alphabet"])} (characters).")    
        else:
            print("❌ Something went wrong! Alphabet could not be written to internal json file.") 

    @staticmethod
    def del_entry_from_jsonfile(json_filename: str, key: str):
        _dict = JsonUtils.load_dict_from_jsonfile(json_filename, "") 
        
        if key not in _dict:
            print(f"The specified key [{key}] has not been found in the given json file.")
            return    
        
        _dict.pop(key, None)    
        json_content = json.dumps(_dict, ensure_ascii=False)
        Path(json_filename).write_text(json_content, encoding="utf8")
    
        check = JsonUtils.load_dict_from_jsonfile(json_filename, "")
        if key not in check:
            print(f"{key} sucessfully deleted from the given json file.")
        else:
            print("Something went wrong. Given entry could not be deleted!")



class AlphabetUtils:
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
       

class WritingSystem:
    @staticmethod
    def by_abugida(abugida: Abugida) -> list[str]:
         _dict = JsonUtils.load_dict_from_jsonfile(JsonFile.Abugida, err_msg_enum_class = "abugidas")
         return _dict[abugida.value[0]]["script"]

    @staticmethod
    def by_syllabary(syllabary: Syllabary) -> list[str]:
         _dict = JsonUtils.load_dict_from_jsonfile(JsonFile.Syllabary, err_msg_enum_class = "syllabaries")
         return _dict[syllabary.value[0]]["script"] 
    
    @staticmethod
    def by_logographic(logographic: Logographic) -> list[str]:
        _dict = JsonUtils.load_dict_from_jsonfile(JsonFile.Logographic, err_msg_enum_class = "logographics")       
        return _dict[logographic.value[0]]["script"]
    

    def by_code(latin_script_code: LatinScriptCode) -> list[tuple[str,str]]:       
        _dict = JsonUtils.load_dict_from_jsonfile(JsonFile.LatinScriptCode, err_msg_enum_class = "latin script codes")
        return _dict[latin_script_code.name]["alphabet"]


    @staticmethod
    def by_language(language: Language, 
                    letter_case: LetterCase = LetterCase.Both,
                    strip_diacritics: bool = False,
                    strip_diphthongs: bool = False) -> str:
       
        # Check if the accociated language code exists within the internal JsonFile.Alphabet file. 
        # If the key is not present, perform a fallback to the Syllabary and Logographic json files and return the respective script.
        _dict = JsonUtils.load_dict_from_jsonfile(JsonFile.Alphabet, err_msg_enum_class = "alphabets")
        language_code = language.value[0]
    
        if language_code not in _dict:

            syllabary_dict = dict([(s.name, s.value[0]) for s in Syllabary])
            logographic_dict = dict([(s.name, s.value[0]) for s in Logographic])

            if language.name in syllabary_dict:                 
                syllabary = Syllabary[language.name]
                alphabet = WritingSystem.by_syllabary(syllabary) 

            elif language.name in logographic_dict:
                logographic = Logographic[language.name]
                alphabet = WritingSystem.by_logographic(logographic) 

        else:
            alphabet = _dict[language_code]["alphabet"]  
        
        # Apply specified filters
        if strip_diacritics:
            diacritics = set(AlphabetUtils.extract_diacritics(alphabet))
            alphabet = [c for c in alphabet if c not in diacritics]

        if strip_diphthongs:
            diphthongs = AlphabetUtils.extract_diphthongs(alphabet)
            alphabet = [c for c in alphabet if c not in diphthongs]

        if letter_case == LetterCase.Lower:
            return [c for c in alphabet if c.islower()] if AlphabetUtils.provides_letter_cases(alphabet) else alphabet
        elif letter_case == LetterCase.Upper:
            return [c for c in alphabet if c.isupper()] if AlphabetUtils.provides_letter_cases(alphabet) else alphabet
        else: 
            return alphabet

