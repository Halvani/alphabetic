from typing import Union, NoReturn
import dcl
import json
from pathlib import Path
from enum import Enum, auto
from .errors import *


class JsonUtils: 

    class FilePath(Enum):
        ISO_639_1_2_Language_Code = r"alphabetic/data/iso_639_1-2_codes_en_de_fr.json",
        Abjad = r"alphabetic/data/abjad.json",
        Abugida = r"alphabetic/data/abugida.json",
        Alphabet = r"alphabetic/data/alphabet.json",
        Featural = r"alphabetic/data/featural.json",
        Latin_Script_Code = r"alphabetic/data/latin_script_code.json",
        Logographic = r"alphabetic/data/logographic.json",    
        Syllabary = r"alphabetic/data/syllabary.json",


    @staticmethod
    def __pluralize(word: str) -> str:
        """
        Pluralizes an English word.

        Args:
            word (str): The word to be pluralized.

        Returns:
            str: The pluralized word.
        """
        
        stem = word[:-1]
        if word.endswith("y") and len(word) > 1 and word[-2] not in set(["a", "e", "i", "o", "u"]):
            return f"{stem}ies"
        elif word.endswith(("o", "ch", "s", "sh", "x", "z")):
            return f"{word}es"
        elif word.endswith("f") and len(word) > 1:
            return f"{stem}ves"
        elif word.endswith("fe") and len(word) > 2:
            stem = word[:-2]
            return f"{stem}ves"
        else:
            return f"{word}s"

    @staticmethod
    def __pluralize_json_filename(json_file: FilePath) -> str:
        if json_file == JsonUtils.FilePath.Latin_Script_Code:
            p = "latin script code".split()
            plural_form = f"{p[0]} {p[1]} {JsonUtils.__pluralize(p[2])}" 
            return plural_form
        else:
            return JsonUtils.__pluralize(json_file.name.lower())


    @staticmethod
    def load_dict_from_jsonfile(json_filename: FilePath) -> dict:
        json_fname = json_filename.value[0]
        if not Path(json_fname).exists():
            err_msg = f"Internal json file: [{json_fname}] could not be found. This file contains all supported {JsonUtils.__pluralize_json_filename(json_filename)}."
            raise FileNotFoundError(err_msg)
        
        json_data = Path(json_fname).read_text(encoding="utf8")
        return json.loads(json_data)
     

    @staticmethod
    def update_lang_json_file(iso_639_code: str, alphabet: list[str]) -> None:

        language_code_db = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.ISO_639_1_2_Language_Code)
        if iso_639_code not in language_code_db:
            raise Non_Existing_ISO_639_2_Langcode(f"Specified language code: [{iso_639_code}] does not exist in the internal ISO 639-1/2 database.")

        json_filename = JsonUtils.FilePath.Alphabet.value[0]
        alphabet_dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Alphabet)
        alphabet_dict[iso_639_code] = {"script": alphabet}
        Path(json_filename).write_text(json.dumps(alphabet_dict, ensure_ascii=False), encoding="utf8")
        created_dict = json.loads(Path(json_filename).read_text(encoding="utf8"))

        if iso_639_code in created_dict:            
            language = language_code_db[iso_639_code][1]
            print(f"✅ Updated json-file successfully!\nLanguage: {language}; "
                  f"Language code: {iso_639_code}; Alphabet size: {len(created_dict[iso_639_code]["script"])} (characters).\n" 
                  f"Note, in order to use this language, you must add the respective entry: {language} = \"{iso_639_code}\" to the enum class Language.")    
        else:
            print("❌ Something went wrong! Alphabet could not be written to internal json file.") 

    @staticmethod
    def del_entry_from_jsonfile(json_file: FilePath, key: str):
        _dict = JsonUtils.load_dict_from_jsonfile(json_file) 

        if key not in _dict:
            raise Non_Existing_ISO_639_2_Langcode(f"❌ Specified key: [{key}] does not exist in the given json file.")  
        
        _dict.pop(key, None)    
        json_content = json.dumps(_dict, ensure_ascii=False)
        Path(json_file.value[0]).write_text(json_content, encoding="utf8")
    
        check = JsonUtils.load_dict_from_jsonfile(json_file)
        if key not in check:
            print(f"✅ Sucessfully deleted the key [{key}] from the json file: {json_file.value[0]}.")
        else:
            print(f"❌ Something went wrong. Given key [{key}] could not be deleted!")




# Notes: 
# -------------------------------
#
# Wrt the writing system types, Alphabetic uses the classification by Daniels and Bright --> Daniels, Peter T.; Bright, William, eds. (1996). The World's Writing Systems. Oxford University Press. ISBN 0-195-07993-0.
#
# The exact relationship between writing systems and languages can be complex. 
# A single language (e.g. Hindustani) can have multiple writing systems, and a writing system can also represent multiple languages. --> https://en.wikipedia.org/wiki/Writing_system
#
# ISO 639 is a standardized nomenclature used to classify languages. Each language is assigned a two-letter (set 1) and three-letter lowercase abbreviation (sets 2–5). 
# Alphabetic uses in almost all cases ISO 639-2 as a language code identifier. However, in cases where no ISO 639-2 fields were available (e.g., "Komi") the ISO 639-3 code was used instead.    
#
# Sources of alphabets --> https://www.omniglot.com/index.htm; https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes    
# Sources of language code listings --> https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes ; https://de.wikipedia.org/wiki/Kategorie:Alphabet
# Overview of all languages in the world listed by categories: https://en.wikipedia.org/wiki/Lists_of_languages
# 
# True alphabets: A true alphabet contains separate letters (not diacritic marks) for both consonants and vowels. --> https://en.wikipedia.org/wiki/List_of_writing_systems#Syllabaries
# Languages without casing distinction: Amharic, Arabic, Assamese, Azerbaijani, Brahui, Balinese, Baluchi, Batak, Baybayin, Bengali, Bilen, Burmese, Chinese, Georgian, Gujarati, Gurmukhi, Hebrew, Hindi, Japanese, Kannada, Kashmiri, Khmer, Korean, Kurdish, Central, Lao, Lontara, Malayalam, Middle Brahmi, Odia, Pashto, Persian, Punjabi, Sindhi, Sinhala, Sundanese, Sylheti, Tamil, Telugu, Thai, Tibetan, Tigre, Tigrinya, Tirhuta, Urdu, Uyghur, Yiddish   --> https://www.quora.com/Which-languages-have-no-capitalized-letter
# Diacritical marks: A number of languages (e.g., French, German, Spanish, Italian, Portuguese, Polish, Czech, Swedish, etc.) make use of diacritics. --> https://entnemdept.ufl.edu/frank/kiss/kiss3.htm
#
# Featural: A featural script represents finer detail than an alphabet. Here, symbols do not represent whole phonemes, but rather the elements (features) that make up the phonemes, such as voicing or its place of articulation. In the Korean alphabet, the featural symbols are combined into alphabetic letters, and these letters are in turn joined into syllabic blocks, so the system combines three levels of phonological representation.  --> https://en.wikipedia.org/wiki/Featural_writing_system
# Amharic: Amharic script is an abugida, and the graphemes of the Amharic writing system are called fidäl. It is derived from a modification of the Ge'ez script. --> https://en.wikipedia.org/wiki/Amharic
# 
# Cree: This language is considered to be a Syllabary according to: https://en.wikipedia.org/wiki/Cree_(language)#Writing 
# However, no ISO-15924 identifier can be found for it under: https://en.wikipedia.org/wiki/ISO_15924 Hencee, it is treated here as an alphabet.
#
# Japanese: There is no alphabet in Japanese. In fact, there are three writing systems called Hiragana, Katakana and Kanji. Katakana and Hiragana constitute syllabaries; 
# Katakana are primarily used to write foreign words, plant and animal names, and for emphasis. --> https://en.wikipedia.org/wiki/Japanese_language#Writing_system
#
# Javanese: Javanese can also be written with the Arabic script (known as the Pegon script) and today generally uses Latin script instead of Javanese script for practical purposes. --> https://en.wikipedia.org/wiki/Javanese_language#Writing_system
# Chinese: According to Britannica, Chinese represents a logographic writing system -->  https://www.britannica.com/topic/Chinese-writing
# 
# Korean: Korean alphabet's (Hangul) has been described as a syllabic alphabet as it combines the features of alphabetic and syllabic writing systems. --> https://en.wikipedia.org/wiki/Korean_language#Writing_system
#
# Moldovan and Romanian share the same alphabet and language code ("rum") --> https://en.wikipedia.org/wiki/Moldovan_language
#
# Hindi: Hindi is written in the Devanagari script --> https://en.wikipedia.org/wiki/Devanagari
#
# Balochi: The Balochi Standard Alphabet is classified as an Abjad script type. However, it is unclear if it falls under the ISO-15924 identifier "Arab". 
# Therefore, it will used here as an Abjad but with its ISO 639-2 language code: "bal" 
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



class WritingSystem:
    # Example: "Deva" -> ["hin", ...]
    iso_15924_to_iso_639_2_3 = { "Hang" : set(["kor", "jje"]), }

    def __jsonfiles_present__(self) -> NoReturn:
        json_filepaths = [x.value[0] for x in JsonUtils.FilePath]

        missing_jsonfiles = []
        for json_filepath in json_filepaths:
            if not Path(json_filepath).exists():
                missing_jsonfiles.append(json_filepath)

        if len(missing_jsonfiles) == 1:
            raise FileNotFoundError(f"Json file: [{missing_jsonfiles[0]}] was not found. Ensure this file exists before performing the instantiation.")
        elif len(missing_jsonfiles) > 1:
            raise FileNotFoundError(f"The following json files: {missing_jsonfiles} were not found. Ensure these files exists before performing the instantiation.")
 

    def __init__(self) -> NoReturn:
        self.__jsonfiles_present__()


    class Language(Enum):
        Abkhazian = "abk", # Script type: Alphabet; Writing system: Cyrillic script
        Afar = "aar", # Script type: Alphabet; Writing system: Latin script
        Afrikaans = "afr", # Script type: Alphabet; Writing system: Latin script
        Albanian = "sqi", # Script type: Alphabet; Writing system: Latin script
        Amharic = "amh",  # Script type: Abugida; Writing system: Geʽez script (slightly derivated)
        Arabic = "ara", # Script type: Abjad; Writing system: Arabic alphabet, Others: Latin script (Arabizi, Said Akl's alphabet,  Hassaniya alphabet, Maltese alphabet, Cypriot Maronite Latin alphabet), Hebrew alphabet (in Israel for Levantine), Syriac alphabet (Garshuni), Greek alphabet (Cypriot Maronite Greek alphabet) 
        Armenian = "arm", # Script type	Alphabet: Writing system: Armenian alphabet
        Assamese = "asm", # Script type	Abugida; Writing system: Bengali–Assamese script 
        Avar = "ava", # Script type: Alphabet; Writing system: Cyrillic (current)
        Avestan = "ave", # Script type: Alphabet; Writing system: Avestan alphabet
        Bambara = "bam", # Script type: Alphabet; Writing system: Latin script (current), Arabic (Ajami), N'ko
        Bashkir = "bak", # Script type: Alphabet; Writing system: Cyrillic (Bashkir alphabet)
        Basque = "baq", # Script type: Alphabet; Writing system: Basque alphabet
        Belarusian = "bel", # Script type: Alphabet; Writing system: Cyrillic (Belarusian alphabet), Belarusian Latin alphabet, Belarusian Braille, Belarusian Arabic alphabet
        Bislama = "bis", # Script type: Alphabet; Writing system: Latin, Avoiuli (local)
        Boko = "bqc", # Script type: Alphabet; Writing system: Latin script
        Bosnian = "bos", # Script type: Alphabet; Writing system: Latin (Gaj's alphabet), Cyrillic (Vuk's alphabet), Yugoslav Braille, Formerly: Arabic (Arebica), Bosnian Cyrillic (Bosančica)
        Breton = "bre", # Script type: Alphabet; Writing system: Latin script (Breton alphabet)
        Bulgarian = "bul", # Script type: Alphabet; Writing system: Cyrillic (Bulgarian alphabet, since 893), Latin (Banat Bulgarian Alphabet) (Banat Bulgarian dialect), Bulgarian Braille
        Buryat = "bua", # Script type: Alphabet; Writing system: Cyrillic, Mongolian script, Vagindra script, Latin script
        Catalan = "cat", # Script type: Alphabet; Writing system: Latin script (Catalan alphabet), Catalan Braille
        Chamorro = "cha", # Script type: Alphabet; Writing system: Latin script
        Chechen = "che", # Script type: Alphabet; Writing system: Cyrillic script (present, official), Latin script (historically), Arabic script (historically), Georgian script (historically)
        Cherokee = "chr", # Script type	Syllabary; Writing system: Cherokee Syllabary 
        Chichewa = "nya", # Script type: Alphabet; Writing system: Latin (Chewa alphabet), Mwangwego, Chewa Braille
        Chinese_Simplified = "chi", # Script type: Logographic; Writing system: Chinese characters, Bopomofo, Pinyin, Xiao'erjing, Dungan, Chinese Braille, ʼPhags-pa script
        Chukchi = "ckt", # Script type: Alphabet; Writing system: Cyrillic script, Tenevil (Historically)
        Chuvash = "chv", # Script type: Alphabet; Writing system: Cyrillic
        Corsican = "cos", # Script type: Alphabet; Writing system: Latin script (Corsican alphabet)
        Cree = "cre", # Writing system: Latin, Canadian Aboriginal syllabics (Cree)
        Croatian = "hrv", # Script type: Alphabet; Writing system: Latin (Gaj's alphabet), Yugoslav Braille, Glagolitic (historical), Bosnian cyrillic (historical)
        Czech = "ces", # Script type: Alphabet; Writing system: Latin script (Czech alphabet), Czech Braille
        Danish = "dan", # Script type: Alphabet; Writing system: Latin (Danish alphabet), Danish Braille
        Dungan = "dng", # Script type: Alphabet; Writing system: Cyrillic (official), Chinese characters (obsolete), Xiao'erjing (obsolete), Latin (historical)
        Dutch = "nld", # Script type: Alphabet; Writing system: Latin (Dutch alphabet), Dutch Braille
        Dzongkha = "dzo", # Script type: Abugida; Writing system: Tibetan script, Dzongkha Braille
        English = "eng", # Script type: Alphabet; Writing system: Latin script
        Esperanto = "epo", # Script type: Alphabet; Writing system: Latin script (Esperanto alphabet), Esperanto Braille
        Estonian = "est", # Script type: Alphabet; Writing system: Latin (Estonian alphabet), Estonian Braille
        Ewe = "ewe", # Script type: Alphabet; Writing system: Latin (Ewe alphabet), Ewe Braille
        Faroese = "fao", # Script type: Alphabet; Writing system: Latin (Faroese alphabet), Faroese Braille
        Fijian = "fij", # Script type: Alphabet; Writing system: Latin-based
        Finnish = "fin", # Script type: Alphabet; Writing system: Latin (Finnish alphabet), Finnish Braille
        French = "fra", # Script type: Alphabet; Writing system: Latin script (French alphabet), French Braille
        Scottish_Gaelic = "gla", # Script type: Alphabet; Writing system: Latin (Scottish Gaelic alphabet), Insular script (historically), Ogham (historically)  
        Georgian = "kat", # Script type: Alphabet; Writing system: Georgian script, Georgian Braille
        Parthian  = "xpr", # Script type: Abjad; Writing system: Inscriptional Parthian, Manichaean script
        Irish = "gle", # Script type: Alphabet; Writing system: Writing system: Latin (Irish alphabet), Ogham (historically), Irish Braille
        German = "deu", # Script type: Alphabet; Writing system: Latin script (German alphabet), German Braille, Until the seventh/eighth century: Runic, Until the mid-20th century: Hebrew Alphabet
        Greek = "gre", # Script type: Alphabet; Writing system: Greek alphabet       
        Balochi = "bal", # Script type: Abjad; Writing system: Balochi Standard Alphabet
        Guarani = "grn", # Script type: Alphabet; Writing system: Guarani alphabet (Latin script)
        Haitian_Creole = "hat", # Script type: Alphabet; Writing system: Latin (Haitian Creole alphabet)
        Hausa = "hau", # Script type: Alphabet; Writing system: Latin (Boko alphabet), Arabic (Hausa Ajami), Hausa Braille
        Hawaiian = "haw", # Script type: Alphabet; Writing system: Latin (Hawaiian alphabet), Hawaiian Braille
        Hebrew = "heb", # Script type: Abjad; Writing system: Hebrew alphabet, Hebrew Braille, Paleo-Hebrew alphabet (Archaic Biblical Hebrew), Imperial Aramaic script (Late Biblical Hebrew), Samaritan script (Samaritan Biblical Hebrew)
        Herero = "her", # Script type: Alphabet; Writing system: Latin (Herero alphabet), Herero Braille
        Hindi = "hin", # Script type: Abugida; Writing system: Devanagari (official), Kaithi (historical), Mahajani (historical), Laṇḍā (historical), Latin (Hinglish, unofficial), Devanagari Braille
        Angika = "anp", # Script type: Abugida; Writing system: Devanagari (official) 
        Boro = "brx", # Script type: Abugida; Writing system: Devanagari (official), Eastern Nagari (contemporary), Latin (contemporary)
        Icelandic = "isl", # Script type: Alphabet; Writing system: Latin (Icelandic alphabet), Icelandic Braille
        Igbo = "ibo", # Script type: Alphabet; Writing system: Latin (Önwu alphabet), Nwagu Aneke script, Neo-Nsibidi, Ndebe script, Igbo Braille
        Indonesian = "ind", # Script type: Alphabet; Writing system: Latin (Indonesian alphabet), Indonesian Braille
        Italian = "ita", # Script type: Alphabet; Writing system: Latin script (Italian alphabet), Italian Braille
        Japanese = "jpn", # Script types: Kanji, Hiragana, Katakana; Writing system: Mixed scripts of Kanji (Chinese characters) and Kana (Hiragana, Katakana), Japanese Braille
        Javanese = "jav", # Script type: Alphabet; Writing system: Latin script, Javanese script, Pegon script
        Kabardian = "kbd", # Script type: Alphabet; Writing system: Cyrillic script, Latin script, Arabic script
        Kanuri = "kau", # Script type: Alphabet; Writing system: Latin, Arabic (Ajami)[3]
        Kashubian = "csb", # Script type: Alphabet; Writing system: Latin (Kashubian alphabet)
        Kazakh = "kaz", # Script type: Alphabet; Writing system: Kazakh alphabets (Cyrillic script, Latin script, Arabic script, Kazakh Braille)
        Kinyarwanda = "kin", # Script type: Alphabet; Writing system: Latin
        Kirghiz = "kir", # Script type: Alphabet; Writing system: Kyrgyz alphabets (Cyrillic script, Perso-Arabic script, Kyrgyz Braille)
        Komi = "kpv", # Script type: Alphabet; Writing system: Cyrillic, Old Permic (formerly)
        Samaritan = "smp", # Script type Abjad; Writing system: Samaritan abjad
        Korean = "kor", # Script type: Featural alphabet; Writing system: Hangul / chosŏn'gŭl (Korean script); Hanja / hancha (auxiliary script for disambiguation [South Korea], historical in North Korea)
        Jeju = "jje", # Script type: Featural alphabet; Writing system: Hangul
        Osage = "osa", # Script type: Alphabet; Writing system: Latin (Osage alphabet), Osage script        
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
        Aleut = "ale",
        Portuguese = "por",
        Phoenician = "phn",
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
        Arapaho = "arp",
        Tuvan = "tyv",
        Twi = "twi",
        Ukrainian = "ukr",
        Uzbek = "uzb",
        Venda = "ven",
        Volapük = "vol",
        Welsh = "wel",
        Wolof = "wol",
        Ugaritic = "uga",
        Yakut = "sah",
        Yiddish = "yid",
        Zulu = "zul",

   
    # Values represent ISO-15924 identifiers
    class Abjad(Enum):
        Balochi = "bal", # Note, no ISO-15924 identifier available
        Hebrew_Samaritan = "Samr",
        Phoenician  = "Phnx",
        Parthian = "Prti",
        Ugaritic  = "Ugar",
        Hebrew = "Hebr",
        Arabic = "Arab",

    # Values represent ISO-15924 or (if not available/present for the respective language) ISO 639-2/3 identifiers !
    class Abugida(Enum):
        Boro = "brx",
        Hindi = "hin",
        Angika = "anp",
        Devanagari = "Deva", # Languages: Apabhramsha, Angika, Awadhi, Bajjika, Bhili, Bhojpuri, Boro, Braj, Chhattisgarhi, Dogri, Garhwali, Haryanvi, Hindi, Kashmiri, Khandeshi, Konkani, Kumaoni, Magahi, Maithili, Marathi, Marwari, Mundari, Nagpuri, Newari, Nepali, Pāli, Pahari, Prakrit, Rajasthani, Sanskrit, Santali, Saraiki, Sherpa, Sindhi, Surjapuri, and many more.
        Dzongkha = "dzo",
        Amharic = "amh",
        Sundanese = "Sund",
        Malayalam = "Mlym",
        Javanese = "Java",
        Assamese = "asm",
        Thaana = "Thaa",

    # Values represent ISO-15924 identifiers. These represent the keys within the json file.  
    class Syllabary(Enum):
        Avestan = "Avst",
        Ethiopic = "Ethi",
        Carian = "Cari",
        Lydian = "Lydi",
        Hiragana = "Hira",
        Cherokee = "Cher",
        Katakana = "Kana",

    # Values represent ISO-15924 identifiers. These represent the keys within the json file. 
    class Logographic(Enum):    
        Kanji = "Hani",
        Chinese_Simplified = "Hans",
    

    class Featural (Enum):
        Hangul = "Hang",

    def pretty_print(self, script_dict: dict, show_script_key: bool = False) -> NoReturn:
        for key in script_dict.keys():
            if show_script_key:
                print(f"{key}:")
                
            print(*script_dict[key])
            
            if len(script_dict.keys()) > 1:
                print()


    class MultigraphSize(Enum):
        All = 2, 7, # All from below (range: [2; 7])
        Digraph = 2, # Two letters, as English ⟨ch⟩ or ⟨ea⟩)
        Trigraph = 3, # Three letters, as French ⟨tch⟩ or ⟨eau⟩)
        Tetragraph = 4, # Four letters, as German ⟨tsch⟩)
        Pentagraph = 5, # Five letters, as Avar ⟨чӀчӀв⟩)
        Hexagraph = 6, # Six letters, as Irish ⟨oidhea⟩)
        Heptagraph = 7 # Seven letters, as German ⟨schtsch⟩)

    class LetterCase(Enum):
        Lower = auto(),
        Upper = auto(),
        Both = auto()


    class LatinScriptCode(Enum):
        Morse = auto(),
        NATO_Phonetic_Alphabet = auto(), 


    def by_abjad(self, abjad: Abjad, as_list: bool = False) -> Union[dict, list[str]]:
         _dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Abjad)
         iso_name, script = abjad.value[0], _dict[abjad.value[0]]["script"]
         return script if as_list else {iso_name : script}


    def by_abugida(self, abugida: Abugida, as_list: bool = False) -> Union[dict, list[str]]:
         _dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Abugida)
         iso_name, script = abugida.value[0], _dict[abugida.value[0]]["script"]
         return script if as_list else {iso_name : script}


    def by_syllabary(self, syllabary: Syllabary, as_list: bool = False) -> Union[dict, list[str]]:
         _dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Syllabary)
         iso_name, script = syllabary.value[0], _dict[syllabary.value[0]]["script"]
         return script if as_list else {iso_name : script}
    

    def by_logographic(self, logographic: Logographic, as_list: bool = False) -> Union[dict, list[str]]:
        _dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Logographic)       
        iso_name, script = logographic.name, _dict[logographic.value[0]]["script"]
        return script if as_list else {iso_name : script}
    

    def by_featural(self, featural: Featural, as_list: bool = False) -> Union[dict, list[str]]:
        _dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Featural)       
        iso_name, script = featural.value[0], _dict[featural.value[0]]["script"]
        return script if as_list else {iso_name : script}
    

    def by_code(self, latin_script_code: LatinScriptCode) -> list[tuple[str,str]]:       
        _dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Latin_Script_Code)
        return _dict[latin_script_code.name]["script"]


    def provides_letter_cases(self, alphabet: list[str]) -> bool:
        return True if len([c for c in alphabet if c.isupper() or c.islower()]) > 0 else False 


    def extract_diacritics(self, alphabet: list[str]) -> list[str]:
        extracted_diacritics = dcl.get_diacritics("".join(alphabet) )
        return [c.character for _, c in extracted_diacritics.items()]
    

    def extract_multigraphs(self, alphabet: list[str], multigraph_size: MultigraphSize) -> list[str]:
        all_ = self.MultigraphSize.All

        if multigraph_size == all_:
            return [c for c in alphabet  if all_.value[0] <= len(c) <= all_.value[1]]
        else:
            return [c for c in alphabet if len(c) == multigraph_size.value[0]]
    

    def get_iso_formal_name(self, iso_15924_group: str, script_type: Enum) -> str:
        for entry in script_type:
            if entry.value[0] == iso_15924_group:
                return entry.name
            

    def by_language(self,
                    language: Language, 
                    letter_case: LetterCase = LetterCase.Both,
                    strip_diacritics: bool = False,
                    strip_multigraphs: bool = False,
                    multigraphs_size: MultigraphSize = MultigraphSize.All,
                    as_list: bool = False) -> Union[list[str], dict]:
       
        # Check if the accociated language code exists within the internal JsonFile.Alphabet file. 
        # If the key is not present, perform a fallback to the Syllabary and Logographic json files and return the respective script.
        _dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Alphabet)
        language_code = language.value[0]
    
        if language_code not in _dict:
            # Special case for languages that have *multiple* writing systems and non-mapable language codes. 
            # ---------------------------------------------------------------------------------------
            # Note that for such languages such as Japanese none of the filters below can be applied. 
            # Also, the parameter *as_list* is ignored, as otherwise it is difficult to understand which list refers to which writing system. 
            # Thus, the respective writing system type(s) is/are returned as they are. 
            if language == self.Language.Japanese:
                return {self.Language.Japanese.name: {self.Syllabary.Hiragana.name: self.by_syllabary(self.Syllabary.Hiragana, as_list=True),
                        self.Syllabary.Katakana.name : self.by_syllabary(self.Syllabary.Katakana, as_list=True),
                        self.Logographic.Kanji.name : self.by_logographic(self.Logographic.Kanji, as_list=True)}}           
                 
            
            abjad_dict = dict([(a.name, a.value[0]) for a in self.Abjad]) 
            abugida_dict = dict([(a.name, a.value[0]) for a in self.Abugida]) 
            syllabary_dict = dict([(s.name, s.value[0]) for s in self.Syllabary])
            logographic_dict = dict([(l.name, l.value[0]) for l in self.Logographic])
            featural_dict = dict([(l.name, l.value[0]) for l in self.Featural])
            
            #TODO: add other writing systems when needed..
            for iso_15924_group, languages in self.iso_15924_to_iso_639_2_3.items():
                if language_code in languages:
                    if iso_15924_group in set([a.value[0] for a in self.Abugida]):
                        iso_formal_name = self.get_iso_formal_name(iso_15924_group, self.Abugida)
                        script = self.by_abugida(self.Abugida[iso_formal_name], as_list=True)
                        return script if as_list else {language.name : script}
                    
                    elif iso_15924_group in set([a.value[0] for a in self.Featural]):
                        iso_formal_name = self.get_iso_formal_name(iso_15924_group, self.Featural)
                        script = self.by_featural(self.Featural[iso_formal_name], as_list=True)
                        return script if as_list else {language.name : script}

            if language.name in syllabary_dict:
                script = self.by_syllabary(self.Syllabary[language.name], as_list=True)
                return script if as_list else {language.name : script} 

            elif language.name in logographic_dict:
                script = self.by_logographic(self.Logographic[language.name], as_list=True)
                return script if as_list else {language.name : script}
            
            elif language.name in featural_dict:
                script = self.by_featural(self.Featural[language.name], as_list=True)
                return script if as_list else {language.name : script}

            elif language.name in abjad_dict:
                script = self.by_abjad(self.Abjad[language.name], as_list=True)
                return script if as_list else {language.name : script}

            elif language.name in abugida_dict:
                script = self.by_abugida(self.Abugida[language.name], as_list=True)
                return script if as_list else { language.name : script}
        else:
            alphabet = _dict[language_code]["script"]

        
        # Apply specified filters
        # ---------------------------------------------------------------------------------------
        if strip_diacritics:
            diacritics = set(self.extract_diacritics(alphabet))
            alphabet = [c for c in alphabet if c not in diacritics]

        # Multigraph: https://en.wikipedia.org/wiki/Multigraph_(orthography)
        if strip_multigraphs: 
            multigraphs = self.extract_multigraphs(alphabet, multigraphs_size)
            alphabet = [c for c in alphabet if c not in multigraphs]

        if letter_case == self.LetterCase.Lower and self.provides_letter_cases(alphabet):
            alphabet = [c for c in alphabet if c.islower()] 

        elif letter_case == self.LetterCase.Upper and self.provides_letter_cases(alphabet):
            alphabet = [c for c in alphabet if c.isupper()]

        return alphabet if as_list else {language.name : alphabet}