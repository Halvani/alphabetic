import os
import re
import dcl
import json
from jamo import h2j, j2hcj
from pathlib import Path
from enum import Enum, auto
from typing import Union, NoReturn
from .errors import Non_Existing_ISO_639_2_Langcode

module_dir = os.path.dirname(os.path.abspath(__file__))

class JsonUtils:
    """Provides utility functions for working with writing systems and scripts embeddedd in JSON data."""
    
    class FilePath(Enum):
        """An enumeration containing file paths for internal JSON data on specific writing systems."""

        Abjad = os.path.normpath(os.path.join(module_dir, "data/abjad.json")),
        Abugida = os.path.normpath(os.path.join(module_dir, "data/abugida.json")),
        Alphabet = os.path.normpath(os.path.join(module_dir, "data/alphabet.json")),
        Featural = os.path.normpath(os.path.join(module_dir, "data/featural.json")),
        Logographic = os.path.normpath(os.path.join(module_dir, "data/logographic.json")),
        Syllabary = os.path.normpath(os.path.join(module_dir, "data/syllabary.json")),
        Latin_Script_Code = os.path.normpath(os.path.join(module_dir, "data/latin_script_code.json")),
        ISO_639_1_2_Language_Code = os.path.normpath(os.path.join(module_dir, "data/iso_639_1-2_codes_en_de_fr.json")),
        ISO_639_3_Language_Code = os.path.normpath(os.path.join(module_dir, "data/iso_639_3_codes_en.json")),
        ISO_15924_Code = os.path.normpath(os.path.join(module_dir, "data/iso_15924_codes.json")),


    @staticmethod
    def __pluralize(word: str) -> str:
        """
        Converts a given singular noun to its plural form based on standard English grammar rules.

        Parameters:
            word (str): The singular noun to be pluralized.

        Returns:
            str: The plural form of the given noun.

        Examples:
            >>> __pluralize("city")
            'cities'
            >>> __pluralize("bus")
            'buses'
            >>> __pluralize("leaf")
            'leaves'
            >>> __pluralize("knife")
            'knives'
            >>> __pluralize("cat")
            'cats'

        Rules applied:
            - If the word ends with 'y' preceded by a consonant, replace 'y' with 'ies'.
            - If the word ends with 'o', 'ch', 's', 'sh', 'x', or 'z', append 'es'.
            - If the word ends with 'f', replace 'f' with 'ves'.
            - If the word ends with 'fe', replace 'fe' with 'ves'.
            - For all other cases, append 's'.
        """
        
        stem = word[:-1]
        if word.endswith("y") and len(word) > 1 and word[-2] not in set(["a", "e", "i", "o", "u"]):
            return f"{stem}ies"
        if word.endswith(("o", "ch", "s", "sh", "x", "z")):
            return f"{word}es"
        if word.endswith("f") and len(word) > 1:
            return f"{stem}ves"
        if word.endswith("fe") and len(word) > 2:
            stem = word[:-2]
            return f"{stem}ves"
        
        return f"{word}s"

    @staticmethod
    def __pluralize_json_filename(json_file: FilePath) -> str:
        """
        Converts a given json filename to its plural form.

        Parameters:
            json_file (FilePath): The singular filename to be pluralized.

        Returns:
            str: The plural form of the given json filename.
        """
        tokens = json_file.name.split("_")
        return f"{' '.join(tokens[:-1])} {JsonUtils.__pluralize(tokens[-1])}".lower().strip()


    @staticmethod
    def load_dict_from_jsonfile(json_filename: FilePath) -> dict:
        """
        Loads a dictionary from a given JSON file.

        This method reads a JSON file specified by `json_filename` and returns its contents as a dictionary.
        If the file does not exist, a `FileNotFoundError` is raised with an appropriate error message.

        Parameters:
            json_filename (FilePath): A `FilePath` object containing the path to the (internal) JSON file.

        Returns: 
            dict: The contents of the JSON file as a dictionary.

        Raises:
            FileNotFoundError: If the JSON file does not exist.
        """
        json_fname = json_filename.value[0]
        if not Path(json_fname).exists():
            err_msg = f"Internal json file: [{json_fname}] could not be found. This file contains all supported {JsonUtils.__pluralize_json_filename(json_filename)}."
            raise FileNotFoundError(err_msg)

        json_data = Path(json_fname).read_text(encoding="utf8")
        return json.loads(json_data)
     

    @staticmethod
    def update_lang_json_file(iso_name: str, script: list[str]) -> None:
        """
        Updates the alphabet JSON file with the script for a specified ISO 639-2/3 language code.

        This function attempts to update the JSON file containing alphabets with a new script for a specified ISO language code. 
        It first checks if the given ISO language code exists in the ISO 639-1/2 database. If not found, it then checks the ISO 639-3 database.
        If the language code is found in either database, it updates the JSON file with the new script. If the language code is not found in both databases, it raises an exception.

        Parameters:
            iso_name (str): The ISO 639-2/3 language code to update.
            script (list[str]): A list of characters representing the script for the language.

        Raises:
            Non_Existing_ISO_639_2_Langcode: If the specified language code does not exist in both the ISO 639-1/2 and ISO 639-3 databases.
        """
            
        iso_639_2_language_code_db = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.ISO_639_1_2_Language_Code)
        if iso_name not in iso_639_2_language_code_db:
            print(f"Specified language code: [{iso_name}] does not exist in the internal ISO 639-1/2 database. Switching to ISO 639-3 database...")
            iso_639_3_language_code_db = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.ISO_639_3_Language_Code)

            if iso_name not in iso_639_3_language_code_db:
                raise Non_Existing_ISO_639_2_Langcode(f"Specified language code: [{iso_name}] does not exist in both the ISO 639-1/2 and ISO 639-3 databases.")

        json_filename = JsonUtils.FilePath.Alphabet.value[0]
        alphabet_dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Alphabet)
        alphabet_dict[iso_name] = {"script": script}
        Path(json_filename).write_text(json.dumps(alphabet_dict, ensure_ascii=False), encoding="utf8")
        created_dict = json.loads(Path(json_filename).read_text(encoding="utf8"))

        if iso_name in created_dict:
            if iso_name in iso_639_2_language_code_db:
                language_print_name = iso_639_2_language_code_db[iso_name][1]
            elif iso_name in iso_639_3_language_code_db:
                language_print_name = iso_639_3_language_code_db[iso_name]

            print(f"✅ Updated json-file successfully!\nLanguage: {language_print_name}; Language code: {iso_name}; Alphabet size: {len(created_dict[iso_name]['script'])} (characters).\nNote, in order to use this language, you must add the respective entry: {language_print_name} = '{iso_name}' to the enum class Language.")    
        else:
            print("❌ Specified language code: {iso_name} was not found in updated json file!")


    @staticmethod
    def del_entry_from_jsonfile(json_file: FilePath, key: str):
        """
        Deletes an entry from a JSON file specified by the given key.

        This method loads the JSON content from the specified file, checks for the existence of the key, and if found, 
        removes the key-value pair from the dictionary. It then writes the updated dictionary back to the JSON file. 
        Finally, it verifies that the key has been successfully deleted.

        Parameters:
            json_file (FilePath): The path to the JSON file from which the entry should be deleted.
            key (str): The key of the entry to be deleted.

        Raises:
            Non_Existing_ISO_639_2_Langcode: If the specified key does not exist in the JSON file.

        Example:
            json_file = JsonUtils.FilePath.Alphabet            
            key = "haw"
            del_entry_from_jsonfile(json_file, key)

        This will delete the entry with the specified key (Hawaiian language code) from the JSON file if it exists.
        """
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
# Punjabi: The Punjabi language is written in multiple scripts i.e. Gurmukhi (Abugida) and Shahmukhi (Abjad). This phenomenon is also known as synchronic digraphia!
#
# Japanese: There is no alphabet in Japanese. In fact, there are three writing systems called Hiragana, Katakana and Kanji. Katakana and Hiragana constitute syllabaries;
# Katakana are primarily used to write foreign words, plant and animal names, and for emphasis. --> https://en.wikipedia.org/wiki/Japanese_language#Writing_system
#
# Sorani: It is unclear which script type Sorani strictly belongs to. Many Kurdish varieties, mainly Sorani, are written using a modified Persian alphabet with 33 letters introduced by Sa'id Kaban Sedqi. 
# Unlike the Persian alphabet, which is an abjad, Central Kurdish is almost a true alphabet in which vowels are given the same treatment as consonants.
# However, we consider for simplicity the Abjad classification. Compare: https://en.wikipedia.org/wiki/Sorani vs. https://kurdishwriting.com/alphabetpage
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
    
    class Language(Enum):
        Abkhazian = "abk", # Script type: Alphabet; Writing system: Cyrillic script
        Afar = "aar", # Script type: Alphabet; Writing system: Latin script
        Afrikaans = "afr", # Script type: Alphabet; Writing system: Latin script
        Albanian = "sqi", # Script type: Alphabet; Writing system: Latin script
        Aleut = "ale", # Script type: Alphabet; Writing system: Latin (Alaska), Cyrillic (Alaska, Russia)
        Amharic = "amh",  # Script type: Abugida; Writing system: Geʽez script (slightly derivated)
        Angika = "anp", # Script type: Abugida; Writing system: Devanagari (official)
        Arabic = "ara", # Script type: Abjad; Writing system: Arabic alphabet, Others: Latin script (Arabizi, Said Akl's alphabet,  Hassaniya alphabet, Maltese alphabet, Cypriot Maronite Latin alphabet), Hebrew alphabet (in Israel for Levantine), Syriac alphabet (Garshuni), Greek alphabet (Cypriot Maronite Greek alphabet) 
        Arapaho = "arp", # Script type: Alphabet; Writing system: Latin
        Armenian = "arm", # Script type	Alphabet: Writing system: Armenian alphabet
        Assamese = "asm", # Script type	Abugida; Writing system: Bengali–Assamese script
        Avar = "ava", # Script type: Alphabet; Writing system: Cyrillic (current)
        Avestan = "ave", # Script type: Alphabet; Writing system: Avestan alphabet
        Balochi = "bal", # Script type: Abjad; Writing system: Balochi Standard Alphabet
        Bambara = "bam", # Script type: Alphabet; Writing system: Latin script (current), Arabic (Ajami), N'ko
        Bashkir = "bak", # Script type: Alphabet; Writing system: Cyrillic (Bashkir alphabet)
        Basque = "baq", # Script type: Alphabet; Writing system: Basque alphabet
        Bavarian = "bar", # Script type: Alphabet; Writing system: Latin alphabet, Marcomannic (historically)
        Belarusian = "bel", # Script type: Alphabet; Writing system: Cyrillic (Belarusian alphabet), Belarusian Latin alphabet, Belarusian Braille, Belarusian Arabic alphabet
        Bislama = "bis", # Script type: Alphabet; Writing system: Latin, Avoiuli (local)
        Boko = "bqc", # Script type: Alphabet; Writing system: Latin script
        Boro = "brx", # Script type: Abugida; Writing system: Devanagari (official), Eastern Nagari (contemporary), Latin (contemporary)
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
        Cimbrian = "cim", # Script type: Alphabet; Writing system: Latin
        Cornish = "cor", # Script type: Alphabet; Writing system: Latin alphabet
        Corsican = "cos", # Script type: Alphabet; Writing system: Latin script (Corsican alphabet)
        Cree = "cre", # Writing system: Latin, Canadian Aboriginal syllabics (Cree)
        Croatian = "hrv", # Script type: Alphabet; Writing system: Latin (Gaj's alphabet), Yugoslav Braille, Glagolitic (historical), Bosnian cyrillic (historical)
        Czech = "ces", # Script type: Alphabet; Writing system: Latin script (Czech alphabet), Czech Braille
        Danish = "dan", # Script type: Alphabet; Writing system: Latin (Danish alphabet), Danish Braille
        Dungan = "dng", # Script type: Alphabet; Writing system: Cyrillic (official), Chinese characters (obsolete), Xiao'erjing (obsolete), Latin (historical)
        Dutch = "nld", # Script type: Alphabet; Writing system: Latin (Dutch alphabet), Dutch Braille
        Dzongkha = "dzo", # Script type: Abugida; Writing system: Tibetan script, Dzongkha Braille
        Elfdalian = "ovd", # Script type: Alphabet; Writing system: Latin (Elfdalian alphabet), Dalecarlian runes, (until the 20th century)
        English = "eng", # Script type: Alphabet; Writing system: Latin script
        Esperanto = "epo", # Script type: Alphabet; Writing system: Latin script (Esperanto alphabet), Esperanto Braille
        Estonian = "est", # Script type: Alphabet; Writing system: Latin (Estonian alphabet), Estonian Braille
        Ewe = "ewe", # Script type: Alphabet; Writing system: Latin (Ewe alphabet), Ewe Braille
        Faroese = "fao", # Script type: Alphabet; Writing system: Latin (Faroese alphabet), Faroese Braille
        Fijian = "fij", # Script type: Alphabet; Writing system: Latin-based
        Finnish = "fin", # Script type: Alphabet; Writing system: Latin (Finnish alphabet), Finnish Braille
        Flemish = "dut", # Script type: Alphabet; Writing system: Latin (Dutch alphabet), Dutch Braille
        French = "fra", # Script type: Alphabet; Writing system: Latin script (French alphabet), French Braille
        Georgian = "kat", # Script type: Alphabet; Writing system: Georgian script, Georgian Braille
        German = "deu", # Script type: Alphabet; Writing system: Latin script (German alphabet), German Braille, Until the seventh/eighth century: Runic, Until the mid-20th century: Hebrew Alphabet
        Greek = "gre", # Script type: Alphabet; Writing system: Greek alphabet
        Guarani = "grn", # Script type: Alphabet; Writing system: Guarani alphabet (Latin script)
        Haitian_Creole = "hat", # Script type: Alphabet; Writing system: Latin (Haitian Creole alphabet)
        Hausa = "hau", # Script type: Alphabet; Writing system: Latin (Boko alphabet), Arabic (Hausa Ajami), Hausa Braille
        Hawaiian = "haw", # Script type: Alphabet; Writing system: Latin (Hawaiian alphabet), Hawaiian Braille
        Hebrew = "heb", # Script type: Abjad; Writing system: Hebrew alphabet, Hebrew Braille, Paleo-Hebrew alphabet (Archaic Biblical Hebrew), Imperial Aramaic script (Late Biblical Hebrew), Samaritan script (Samaritan Biblical Hebrew)
        Herero = "her", # Script type: Alphabet; Writing system: Latin (Herero alphabet), Herero Braille
        Hindi = "hin", # Script type: Abugida; Writing system: Devanagari (official), Kaithi (historical), Mahajani (historical), Laṇḍā (historical), Latin (Hinglish, unofficial), Devanagari Braille
        Icelandic = "isl", # Script type: Alphabet; Writing system: Latin (Icelandic alphabet), Icelandic Braille
        Igbo = "ibo", # Script type: Alphabet; Writing system: Latin (Önwu alphabet), Nwagu Aneke script, Neo-Nsibidi, Ndebe script, Igbo Braille
        Indonesian = "ind", # Script type: Alphabet; Writing system: Latin (Indonesian alphabet), Indonesian Braille
        Irish = "gle", # Script type: Alphabet; Writing system: Writing system: Latin (Irish alphabet), Ogham (historically), Irish Braille
        Istro_Romanian = "ruo", # Script type: Alphabet; Writing system: Latin
        Italian = "ita", # Script type: Alphabet; Writing system: Latin script (Italian alphabet), Italian Braille
        Japanese = "jpn", # Script types: Kanji, Hiragana, Katakana; Writing system: Mixed scripts of Kanji (Chinese characters) and Kana (Hiragana, Katakana), Japanese Braille
        Javanese = "jav", # Script type: Alphabet; Writing system: Latin script, Javanese script, Pegon script
        Jeju = "jje", # Script type: Featural alphabet; Writing system: Hangul
        Kabardian = "kbd", # Script type: Alphabet; Writing system: Cyrillic script, Latin script, Arabic script
        Kanuri = "kau", # Script type: Alphabet; Writing system: Latin, Arabic (Ajami)[3]
        Kashubian = "csb", # Script type: Alphabet; Writing system: Latin (Kashubian alphabet)
        Kazakh = "kaz", # Script type: Alphabet; Writing system: Kazakh alphabets (Cyrillic script, Latin script, Arabic script, Kazakh Braille)
        Kinyarwanda = "kin", # Script type: Alphabet; Writing system: Latin
        Kirghiz = "kir", # Script type: Alphabet; Writing system: Kyrgyz alphabets (Cyrillic script, Perso-Arabic script, Kyrgyz Braille)
        Komi = "kpv", # Script type: Alphabet; Writing system: Cyrillic, Old Permic (formerly)
        Korean = "kor", # Script type: Featural alphabet; Writing system: Hangul / chosŏn'gŭl (Korean script); Hanja / hancha (auxiliary script for disambiguation [South Korea], historical in North Korea)
        Kumyk = "kum", # Script type: Alphabet; Writing system: Cyrillic, Latin, Arabic
        Kurmanji = "kmr", # Script type: Alphabet; Writing system: Hawar alphabet (Latin) in Turkey, Syria, Iraq and Iran, Sorani alphabet (Arabic) in Iraq and Iran, Cyrillic script in Russia and Armenia
        Latin = "lat", # Script type: Alphabet; Writing system: Latin alphabet (Latin script)
        Latvian = "lav", # Script type: Alphabet; Writing system: Latin (Latvian alphabet), Latvian Braille
        Lezghian = "lez", # Script type: Alphabet; Writing system: Cyrillic (1938–present), Latin (1928–38), Arabic (before 1928)
        Lingala = "lin", # Script type: Alphabet; Writing system: African reference alphabet (Latin), Mandombe script
        Lithuanian = "lit", # Script type: Alphabet; Writing system: Latin (Lithuanian alphabet), Lithuanian Braille
        Luganda = "lug", # Script type: Alphabet; Writing system: Latin script (Ganda alphabet), Ganda Braille
        Luxembourgish = "ltz", # Script type: Alphabet; Writing system: Latin (Luxembourgish alphabet), Luxembourgish Braille
        Macedonian = "mkd", # Script type: Alphabet; Writing system: Cyrillic (Macedonian alphabet), Macedonian Braille
        Malagasy = "mlg", # Script type: Alphabet; Writing system: Latin script (Malagasy alphabet), Sorabe alphabet (Historically), Malagasy Braille
        Malay = "may", # Script type: Alphabet; Writing system: Latin (Malay alphabet), Arabic (Jawi script), Arabic (Pegon script) (In Indonesia), Thai alphabet (in Thailand), Malay Braille, Historically Pallava script, Kawi script, Ulu scripts, Rejang script
        Malayalam = "mal", # Script type: Alphabet; Writing system: Malayalam script (Brahmic), Malayalam Braille, Vatteluttu (historical), Koleluttu (historical), Malayanma (historical), Grantha (historical), Arabi Malayalam script (mostly historical), Suriyani Malayalam (historical), Hebrew script, Latin script (informal)
        Maltese = "mlt", # Script type: Alphabet; Writing system: Latin (Maltese alphabet), Maltese Braille
        Manx = "glv", # Script type: Alphabet; Writing system: Latin
        Maori = "mao", # Script type: Alphabet; Writing system: Latin (Māori alphabet), Māori Braille
        Mari = "chm", # Script type: Alphabet; Writing system: Cyrillic
        Marshallese = "mah", # Script type: Alphabet; Writing system: Latin (Marshallese alphabet)
        Moksha = "mdf", # Script type: Alphabet; Writing system: Cyrillic
        Moldovan = "rum", # Script type: Alphabet; Writing system: Moldovan Cyrillic (Transnistria), Latin alphabet (Ukraine)
        Mongolian = "mon", # Script type: Alphabet; Writing system: Traditional Mongolian (in China and Mongolia), Mongolian Cyrillic (in Mongolia and Russia), Mongolian Braille, ʼPhags-pa (historical, among others)
        Mru = "mro", # Script type: Alphabet; Writing system: Mru script, Latin script
        Nepali = "nep", # Script type: Abugida; Writing system: Devanagari, Devanagari Braille
        Norwegian = "nor", # Script type: Alphabet; Writing system: Latin (Norwegian alphabet), Norwegian Braille
        Occitan = "oci", # Script type: Alphabet; Writing system: Latin alphabet (Occitan alphabet)
        Oromo = "orm", # Script type: Alphabet; Writing system: Latin (Qubee, Oromo alphabet), Qubee Sheek Bakrii Saphaloo
        Osage = "osa", # Script type: Alphabet; Writing system: Latin (Osage alphabet), Osage script
        Parthian  = "xpr", # Script type: Abjad; Writing system: Inscriptional Parthian, Manichaean script
        Pashto = "pus", # Script type: Abjad; Writing system: Pashto alphabet
        Persian = "per", # Script type: Abjad; Writing system: Persian alphabet (Iran and Afghanistan), Tajik alphabet (Tajikistan), Old Persian cuneiform (525 BC – 330 BC), Pahlavi scripts (2nd century BC to 7th century AD), Persian Braille
        Phoenician = "phn", # Script type: Abjad; Writing system: Phoenician alphabet
        Polish = "pol", # Script type: Alphabet; Writing system: Latin (Polish alphabet)
        Portuguese = "por", # Script type: Alphabet; Writing system: Latin (Portuguese alphabet), Portuguese Braille
        Punjabi_Gurmukhī = "_pan", # Script type: Abugida; Writing system: Shāhmukhī (majority, Pakistan), Gurmukhī (official, India), Punjabi Braille
        Punjabi_Shahmukhi = "pan", # Script type: Abjad; Writing system: Shāhmukhī (majority, Pakistan), Gurmukhī (official, India), Punjabi Braille
        Quechua = "que", # Script type: Alphabet; Writing system: Latin (Quechuan alphabet)
        Rohingya = "rhg", # Script type: Alphabet: Writing system: Hanifi Rohingya, Perso-Arabic (Rohingya Arabic Alphabet), Latin (Rohingyalish), Burmese, Bengali–Assamese (rare)
        Russian = "rus", # Script type: Alphabet: Writing system: Cyrillic (Russian alphabet), Russian Braille
        Samaritan = "smp", # Script type Abjad; Writing system: Samaritan abjad
        Samoan = "smo", # Script type: Alphabet; Writing system: Latin (Samoan alphabet), Samoan Braille
        Sango = "sag", # Script type: Alphabet; Writing system: Latin script
        Sanskrit = "san", # Script type: Abugida; Writing system: Devanagari script (present day), Originally orally transmitted, Brahmi script (from 1st century BCE), Brahmic scripts
        Scottish_Gaelic = "gla", # Script type: Alphabet; Writing system: Latin (Scottish Gaelic alphabet), Insular script (historically), Ogham (historically)
        Serbian = "srp", # Script type: Alphabet; Writing system: Serbian Cyrillic, Serbian Latin, Yugoslav Braille
        Slovak = "slo", # Script type: Alphabet; Writing system: Latin (Slovak alphabet), Slovak Braille, Cyrillic (Pannonian Rusyn alphabet)
        Slovenian = "slv", # Script type: Alphabet; Writing system: Latin (Slovene alphabet), Slovene Braille
        Somali = "som", # Script type: Alphabet; Writing system: Somali Latin alphabet (Latin script; official), Wadaad's writing (Arabic script), Osmanya alphabet, Borama alphabet, Kaddare alphabet
        Sorani = "ckb", # Script type: Abjad; Writing system: Kurdo-Arabic alphabet (Persian alphabet), Hawar alphabet (occasionally)
        Spanish = "spa", # Script type: Alphabet; Writing system: Latin script (Spanish alphabet), Spanish Braille
        Sundanese = "sun", # Script type: Abugida; Writing system: Latin script (present), Sundanese script (present; optional), Sundanese Pégon script (17–20th centuries AD, present; religious schools only), Old Sundanese script (14–18th centuries AD, present; optional), Sundanese Cacarakan script (17–19th centuries AD, present; certain areas), Buda Script (13–15th centuries AD, present; optional), Kawi script (historical), Pallava (historical), Pranagari (historical), Vatteluttu (historical)
        Swedish = "swe", # Script type: Alphabet; Writing system: Latin (Swedish alphabet), Swedish Braille
        Swiss_German = "gsw", # Script type: Alphabet; Writing system: Latin
        Tajik = "tgk", # Script type: Alphabet; Writing system: Cyrillic (Tajik alphabet), Historically: Arabic (Persian alphabet), Latin (Yañalif-based), Hebrew (by Bukharan Jews), Tajik Braille
        Tatar = "tat", # Script type: Alphabet; Writing system: Tatar alphabet (Cyrillic, Latin, formerly Arabic)
        Turkish = "tur", # Script type: Alphabet; Writing system: Latin (Turkish alphabet), Turkish Braille
        Turkmen = "tuk", # Script type: Alphabet; Writing system: Latin (Turkmen alphabet, official in Turkmenistan), Perso-Arabic, Cyrillic, Turkmen Braille
        Tuvan = "tyv", # Script type: Alphabet; Writing system: Cyrillic script
        Twi = "twi", # Script type: Alphabet; Writing system: Latin
        Ugaritic = "uga", # Script type	Abjad; Writing system: Ugaritic alphabet
        Ukrainian = "ukr", # Script type: Alphabet; Writing system: Cyrillic (Ukrainian alphabet), Ukrainian Braille
        Uzbek = "uzb", # Script type: Alphabet; Writing system: Latin (Uzbek alphabet), Cyrillic, Perso-Arabic, Uzbek Braille, (Uzbek alphabets)
        Venda = "ven", # Script type: Alphabet; Writing system: Latin (Venda alphabet), Venda Braille, Ditema tsa Dinoko
        Vengo = "bav", # Script type: Alphabet; Writing system: Latin
        Volapük = "vol", # Script type: Alphabet; Writing system: Latin
        Welsh = "wel", # Script type: Alphabet; Writing system: Latin (Welsh alphabet), Welsh Braille
        Wolof = "wol", # Script type: Alphabet; Writing system: Latin (Wolof alphabet), Arabic (Wolofal), Garay
        Yakut = "sah", # Script type: Alphabet; Writing system: Cyrillic (formerly Latin and Cyrillic-based)
        Yiddish = "yid", # Script type: Abjad; Writing system: Hebrew alphabet (Yiddish orthography), occasionally Latin alphabet
        Zeeuws = "zea", # Script type: Alphabet; Writing system: Zeelandic alphabet (Latin)
        Zulu = "zul", # Script type: Alphabet; Writing system: Latin (Zulu alphabet), Zulu Braille, Ditema tsa Dinoko
    
   
    # Values represent ISO-15924 identifiers
    class Abjad(Enum):
        Sorani = "ckb",
        Punjabi_Shahmukhi = "pan",
        Persian = "per",
        Pashto = "pus",
        Ugaritic = "Ugar",
        Balochi = "bal", # Note, no ISO-15924 identifier available
        Samaritan = "Samr",
        Phoenician  = "Phnx",
        Parthian = "Prti",
        Yiddish = "yid", # Yiddish represents a modified version of the Hebrew script, with all vowels rendered in the spelling, except in the case of inherited Hebrew words, which typically retain their Hebrew consonant-only spellings. 
        Hebrew = "Hebr",
        Arabic = "Arab",
    

    # Values represent ISO-15924 or (if not available/present for the respective language) ISO 639-2/3 identifiers !
    class Abugida(Enum):
        Sanskrit = "san", # Tests ✔️
        Punjabi_Gurmukhī = "Guru", # Tests ✔️
        Nepali = "nep", # Tests ✔️
        Boro = "brx", # Tests ✔️
        Hindi = "hin", # Tests ✔️
        Angika = "anp", # Tests ✔️
        Devanagari = "Deva", # Tests ✔️   # Languages: Apabhramsha, Angika, Awadhi, Bajjika, Bhili, Bhojpuri, Boro, Braj, Chhattisgarhi, Dogri, Garhwali, Haryanvi, Hindi, Kashmiri, Khandeshi, Konkani, Kumaoni, Magahi, Maithili, Marathi, Marwari, Mundari, Nagpuri, Newari, Nepali, Pāli, Pahari, Prakrit, Rajasthani, Sanskrit, Santali, Saraiki, Sherpa, Sindhi, Surjapuri, and many more.
        Dzongkha = "dzo", # Tests ❌
        Amharic = "amh", # Tests ✔️
        Sundanese = "Sund", # Tests ✔️
        Malayalam = "Mlym", # Tests ✔️
        Assamese = "asm", # Tests ✔️
        Thaana = "Thaa", # Tests ✔️
        Ethiopic = "Ethi",


    # Values represent ISO-15924 identifiers. These represent the keys within the json file.
    class Syllabary(Enum):
        Avestan = "Avst",
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


    def __jsonfiles_present(self) -> NoReturn:
        """
        Checks the presence of required JSON files and raises an error if any are missing.

        This method iterates through a list of file paths obtained from `JsonUtils.FilePath`.
        It checks if each file exists at the specified path. If one or more files are missing,
        it raises a `FileNotFoundError` with a message indicating which files were not found.

        Raises:
            FileNotFoundError: If one or more JSON files are not found. The error message
            will specify the missing file(s).

        Example:
            # Assume `JsonUtils.FilePath` contains paths to necessary JSON files.
            self.__jsonfiles_present__()
            
            # If one or more files are missing, a respective FileNotFoundError will be raised:
            # FileNotFoundError: Json file: [missing_file.json] was not found. Ensure this file exists before performing the instantiation.
            # FileNotFoundError: The following json files: ['missing_file1.json', 'missing_file2.json'] were not found. Ensure these files exists before performing the instantiation.
        """

        json_filepaths = [x.value[0] for x in JsonUtils.FilePath]

        missing_jsonfiles = []
        for json_filepath in json_filepaths:
            if not Path(json_filepath).exists():
                missing_jsonfiles.append(json_filepath)

        if len(missing_jsonfiles) == 1:
            raise FileNotFoundError(f"Json file: [{missing_jsonfiles[0]}] was not found. Ensure this file exists before performing the instantiation.")
        if len(missing_jsonfiles) > 1:
            raise FileNotFoundError(f"The following json files: {missing_jsonfiles} were not found. Ensure these files exists before performing the instantiation.")
 

    def __mapping_writing_systems_to_scripts(self) -> dict:
        """Generates a dictionary mapping of writing systems to sets of unique script characters.

        This method retrieves data from pre-defined JSON files associated with different writing systems 
        (defined in the `FilePath` enum of the `JsonUtils` class) and processes it to create the final dictionary.

        Returns:
            dict: A dictionary where keys are writing system names (obtained from the file paths) and 
            values are sets containing unique characters from all scripts within that writing system.

        Raises:
            (Implicit) Any exceptions raised by the `load_dict_from_jsonfile` function used for loading JSON data. 
        """

        writing_systen_json_filepaths = [
            JsonUtils.FilePath.Abjad,
            JsonUtils.FilePath.Abugida,
            JsonUtils.FilePath.Alphabet,
            JsonUtils.FilePath.Syllabary,
            JsonUtils.FilePath.Logographic,
            JsonUtils.FilePath.Featural]
        
        writing_systen_map_script = {w.name:list(JsonUtils.load_dict_from_jsonfile(w).values()) for w in writing_systen_json_filepaths}
        return {ws_name:set(list("".join(["".join(d['script']) for d in script]))) for ws_name, script in writing_systen_map_script.items()}


    def __init__(self) -> NoReturn:
        self.__jsonfiles_present()
        self.writing_systems_to_scripts = self.__mapping_writing_systems_to_scripts()
        self.iso_15924_to_iso_639_2_3 = { "Hang" : set(["kor", "jje"]), } # Required for fallback strategy (ISO 639-2/3 language code --> ISO 15924)


    def iso_code_to_name(self, iso_code: str) -> str:
        """
        Convert an ISO 639-2/3 or ISO 15924 code to its corresponding language or script name.

        This function takes an ISO code as input and returns the corresponding name based on the code type.
        It supports both ISO 639-2/3 language codes and ISO 15924 script codes.

        Parameters:
            iso_code (str): An ISO 639-2/3 or ISO 15924 code.

        Returns:
            str: The corresponding language or script name.

        Raises:
            ValueError: If the given input is not a valid ISO 639-2/3 or ISO 15924 code.

        Notes:
            - For ISO 639-2/3 codes, it loads dictionaries from JSON files to map the codes to language names.
            - For ISO 15924 codes, it loads a dictionary from a JSON file to map the codes to script names.
            - ISO 639-2/3 codes are three letters long.
            - ISO 15924 codes are four letters long.

        Example:
            iso_code_to_name('deu') -> 'German'
            iso_code_to_name('Hang') -> 'Hangul (Hangŭl, Hangeul)'
        """
        iso_code = iso_code.strip()

        # Assume we are given an ISO 639-2/3 code.
        if len(iso_code) == 3:
            iso_639_1_2_dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.ISO_639_1_2_Language_Code)
            iso_639_3_dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.ISO_639_3_Language_Code)

            if iso_code in iso_639_1_2_dict:
                return iso_639_1_2_dict[iso_code][1]
            elif iso_code in iso_639_3_dict:
                lang = iso_639_3_dict[iso_code]
                return lang.split(";")[0]

        elif len(iso_code) == 4:
            iso_15924_dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.ISO_15924_Code)
            
            if iso_code in iso_15924_dict:
                return iso_15924_dict[iso_code]
        else:
            raise ValueError(f"The specified string [{iso_code}] does not appear to represent a valid ISO 639-2/3 or ISO 15924 code.")


    def decompose_korean_char_sequence(self, sequence: str) -> str:
        """
        Decompose a sequence of Korean characters into their constituent Hangul Jamo components.

        This function takes a string of Korean characters (Hangul syllables) and decomposes
        each character into its constituent Jamo (consonant and vowel) components using
        the `j2hcj` and `h2j` functions.

        Parameters:
        sequence (str): A string of Korean characters to be decomposed.

        Returns:
        str: A string where each Korean character is decomposed into its constituent Jamo components.

        Example:
        >>> decompose_korean_char_sequence("안녕하세요")
        'ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ'
        """
        return j2hcj(h2j(sequence))


    def is_writing_system(self, sequence: str, script_type: str, strip_spaces: bool = True) -> bool:
        """
        Check if a sequence of characters belongs to a specified writing system.

        This function verifies whether all characters in the given sequence are part of the
        specified writing system. It supports multiple writing systems such as Abjad, Abugida,
        Alphabet, Syllabary, Logographic, and Featural. Optionally, spaces can be stripped from 
        the sequence before checking.

        Parameters:
        sequence (str): The input string to be checked.
        script_type (str): The type of writing system to check against. This should be one of 
                        'Abjad', 'Abugida', 'Alphabet', 'Syllabary', 'Logographic', or 'Featural'.
        strip_spaces (bool): Whether to strip spaces from the input string before checking. Default is True.

        Returns:
        bool: True if all characters in the sequence belong to the specified writing system, False otherwise.

        Raises:
        ValueError: If an unknown writing system type is provided.

        Example:
        >>> is_writing_system('안녕하세요', 'Alphabet')
        False
        >>> is_writing_system('abcdef', 'Alphabet')
        True
        >>> is_writing_system('مرحبا', 'Abjad')
        True
        >>> is_writing_system('안녕하세요', 'Featural')
        True
        """
        if sequence and strip_spaces:
            sequence = re.sub(r"\s+", "", sequence)
        
        # Special case for Hangul (each character must be decomposed into its constituents)
        if script_type == "Featural":
            sequence = self.decompose_korean_char_sequence(sequence)
        
        system_key = self.writing_systems_to_scripts.get(script_type)
        
        if system_key is None:
            raise ValueError(f"Unknown writing system type: {script_type}")
        
        return all(c in system_key for c in sequence)


    def is_alphabet(self, sequence: str, strip_spaces: bool = True) -> bool:
        return self.is_writing_system(sequence, 'Alphabet', strip_spaces)
    
    def is_abjad(self, sequence: str, strip_spaces: bool = True) -> bool:
        return self.is_writing_system(sequence, self.Abjad.__name__, strip_spaces)

    def is_abugida(self, sequence: str, strip_spaces: bool = True) -> bool:
        return self.is_writing_system(sequence, self.Abugida.__name__, strip_spaces)

    def is_syllabary(self, sequence: str, strip_spaces: bool = True) -> bool:
        return self.is_writing_system(sequence, self.Syllabary.__name__, strip_spaces)

    def is_logographic(self, sequence: str, strip_spaces: bool = True) -> bool:
        return self.is_writing_system(sequence, self.Logographic.__name__, strip_spaces)

    def is_featural(self, sequence: str, strip_spaces: bool = True) -> bool:
        return self.is_writing_system(sequence, self.Featural.__name__, strip_spaces)


    def pretty_print(self, script_dict: dict, show_script_key: bool = False) -> NoReturn:
        """
        Pretty print the contents of a dictionary where keys are script names and values are lists of characters.

        This function iterates through the given dictionary and prints the characters in each list. If `show_script_key` 
        is set to True, it also prints the script name (the dictionary key) before the corresponding characters. 
        An extra newline is added between different script lists if the dictionary contains more than one key.

        Parameters:
        script_dict (dict): A dictionary where keys are script names and values are lists of characters.
        show_script_key (bool): Whether to print the script name (key) before the characters. Default is False.

        Returns:
        NoReturn: This function does not return anything. It prints the output directly.

        Example:
        >>> script_dict = {
                'Latin': ['A', 'B', 'C'],
                'Greek': ['Α', 'Β', 'Γ']
            }
        >>> pretty_print(script_dict, show_script_key=True)
        Latin:
        A B C
        
        Greek:
        Α Β Γ
        """
        for key in script_dict.keys():
            if show_script_key:
                print(f"{key}:")
                
            print(*script_dict[key])
            
            if len(script_dict.keys()) > 1:
                print()


    class MultigraphSize(Enum):
        All = 2, 7, # All from below (range: [2; 7])
        Digraph = 2, # Two letters
        Trigraph = 3, # Three letters
        Tetragraph = 4, # Four letters
        Pentagraph = 5, # Five letters
        Hexagraph = 6, # Six letters
        Heptagraph = 7 # Seven letters


    class LetterCase(Enum):
        Lower = auto(),
        Upper = auto(),
        Both = auto()


    class LatinScriptCode(Enum):
        Morse = auto(),
        NATO_Phonetic_Alphabet = auto()


    def text_to_latin_script_code(self,
                                  word_2_translate: str,
                                  latin_script_code: LatinScriptCode,
                                  as_string: bool = False) -> Union[str, list[str]]:
        """
        Convert a given word to its corresponding representation in a specified Latin script code.

        This function translates each character of the input word to its corresponding
        representation in the specified Latin script code. The script code is provided
        as an enumeration value from the `LatinScriptCode` Enum. The result can be
        returned either as a single concatenated string or as a list of individual
        translations.

        Parameters:
            word_2_translate (str): The input word to be translated. The word should
                                    contain only Latin characters (A-Z).
            latin_script_code (LatinScriptCode): The enumeration value representing the
                                                desired Latin script code for translation.
            as_string (bool, optional): If True, the translated word is returned as a
                                        single string. If False, the translated word is
                                        returned as a list of individual translations.
                                        Default is False.

        Returns:
            Union[str, list[str]]: The translated word either as a single concatenated
                                string or as a list of individual translations, based
                                on the value of `as_string`.

        Raises:
            ValueError: If the input string contains invalid characters. Only Latin
                        characters (A-Z) are allowed.

        Example:
            Suppose the Enum `LatinScriptCode` has a value `NATO_Phonetic_Alphabet`
            which translates characters as follows:
            `{'NATO_Phonetic_Alphabet': {'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', ...}}`

            >>> self.text_to_latin_script_code("AB", LatinScriptCode.NATO_Phonetic_Alphabet)
            ['Alfa', 'Bravo']
            
            >>> self.text_to_latin_script_code("AB", LatinScriptCode.NATO_Phonetic_Alphabet, as_string=True)
            'AlfaBravo'
        """        

        alphabet = self.by_language(self.Language.English, as_list=True)

        if not (len(word_2_translate.strip()) > 0 and set(word_2_translate).issubset(set(alphabet))):
            raise ValueError("Invalid characters found in the input string. Only Latin characters (A-Z) are allowed!")

        # By convention, Latin characters are capitalized
        word_2_translate = word_2_translate.upper()

        latin_script_code_alphabet = self.by_code(latin_script_code)
        result = [latin_script_code_alphabet[latin_script_code.name][c] for c in word_2_translate]
        
        return "".join(result) if as_string else result


    def by_script(self, script_type: Union[Abjad, Abugida, Syllabary, Logographic, Featural, LatinScriptCode],
                  as_list: bool = False) -> Union[dict, list[str], list[tuple[str, str]]]:
        """
        Retrieve the script information for a given script type.

        Parameters:
            script_type: The type of script to retrieve information for. This can be an instance of Abjad, Abugida, Syllabary, Logographic, Featural, or LatinScriptCode.
            as_list (bool): Determines the format of the returned script information. If True, returns a list of scripts. If False, returns a dictionary with the ISO name as the key and the script as the value. Defaults to False.

        Returns:
            Union[dict, list[str], list[tuple[str, str]]]: The script information. The format depends on the value of the as_list parameter and the type of script_type provided.
        """
        
        file_path_mapping = {
            self.Abjad: JsonUtils.FilePath.Abjad,
            self.Abugida: JsonUtils.FilePath.Abugida,
            self.Syllabary: JsonUtils.FilePath.Syllabary,
            self.Logographic: JsonUtils.FilePath.Logographic,
            self.Featural: JsonUtils.FilePath.Featural,
            self.LatinScriptCode: JsonUtils.FilePath.Latin_Script_Code,
        }
        
        script_class = type(script_type)
        _dict = JsonUtils.load_dict_from_jsonfile(file_path_mapping[script_class])
        
        if script_class is self.LatinScriptCode:
            return {script_type.name: _dict[script_type.name]["script"]}
                        
        iso_name = script_type.value[0]
        script = _dict[iso_name]["script"]
        
        return script if as_list else {iso_name: script}


    def by_abjad(self, abjad: Abjad, as_list: bool = False) -> Union[dict, list[str]]:
        return self.by_script(abjad, as_list)


    def by_abugida(self, abugida: Abugida, as_list: bool = False) -> Union[dict, list[str]]:
        return self.by_script(abugida, as_list)


    def by_syllabary(self, syllabary: Syllabary, as_list: bool = False) -> Union[dict, list[str]]:
        return self.by_script(syllabary, as_list)


    def by_logographic(self, logographic: Logographic, as_list: bool = False) -> Union[dict, list[str]]:
        return self.by_script(logographic, as_list)


    def by_featural(self, featural: Featural, as_list: bool = False) -> Union[dict, list[str]]:
        return self.by_script(featural, as_list)


    def by_code(self, latin_script_code: LatinScriptCode) -> list[tuple[str,str]]:
        return self.by_script(latin_script_code)
        #_dict = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Latin_Script_Code)
        #return _dict[latin_script_code.name]["script"]


    def has_upper_or_lower_case(self, script: list[str]) -> bool:
        """
        Checks if the provided alphabet (e.g., alphabet) contains any letters with case (upper or lower).

        Parameters:
        -----------
        script : list[str]
            A list of strings representing the script to be checked.

        Returns:
        --------
        bool
            True if the script contains at least one letter that is either uppercase or lowercase, False otherwise.

        Example:
        --------
        >>> ws = WritingSystem()
        >>> has_upper_or_lower_case(ws.by_language(ws.Language.German, as_list=True))
        True
        >>> has_upper_or_lower_case(ws.by_language(ws.Language.Hebrew, as_list=True))
        False
        """
        return any(c.isupper() or c.islower() for c in script)


    def extract_diacritics(self, alphabet: list[str]) -> list[str]:
        """
        Extracts and returns a list of unique diacritic characters from the given list of alphabetic characters.

        Parameters:
            alphabet (list[str]): A list of strings, where each string represents a letter of an alphabet.

        Returns:
            list[str]: A list of unique diacritic characters present in the input alphabet.
        """
        extracted_diacritics = dcl.get_diacritics("".join(alphabet) )
        return [c.character for _, c in extracted_diacritics.items()]


    def extract_multigraphs(self, alphabet: list[str], multigraph_size: MultigraphSize) -> list[str]:
        """
        Extracts multigraphs from a given alphabet based on the specified size constraints. 
        A multigraph (or pleograph) is a sequence of letters that behaves as a unit.  

        Parameters:
        -----------
        alphabet : list[str]
            A list of strings representing the alphabet from which multigraphs are to be extracted.
        multigraph_size : MultigraphSize
            An instance of the MultigraphSize class, which can either specify a specific size for the multigraphs
            or a range of sizes if set to MultigraphSize.All.

        Returns:
        --------
        list[str]
            A list of multigraphs from the given alphabet that match the specified size constraints.

        Notes:
        ------
        - If `multigraph_size` is set to `MultigraphSize.All`, the function returns all strings in the alphabet
        whose lengths fall within the range defined by `MultigraphSize.All.value`.
        - Otherwise, the function returns only those strings whose lengths exactly match `multigraph_size.value[0]`.
        """
        all_ = self.MultigraphSize.All

        if multigraph_size == all_:
            return [c for c in alphabet  if all_.value[0] <= len(c) <= all_.value[1]]        
        return [c for c in alphabet if len(c) == multigraph_size.value[0]]


    def retrieve_iso_formal_name(self, iso_15924_group: str, script_type: Enum) -> str:
        """Retrieves the formal name for a given ISO 15924 group code.

        Parameters:
            iso_15924_group (str): The ISO 15924 group code (e.g., "Cher").
            script_type (Enum): An enumeration representing a script type (e.g., Syllabary).

        Returns:
            str: The formal name of the script system if found, otherwise raises a ValueError.

        Raises:
            ValueError: If no matching entry is found for the provided ISO 15924 group code.
        """
        name_map = {entry.value[0]: entry.name for entry in script_type}
        if iso_15924_group in name_map:
            return name_map[iso_15924_group]
        else:
            raise ValueError(f"No entry found for the ISO 15924 group code: {iso_15924_group}")


    def by_language(self,
                    language: Language,
                    letter_case: LetterCase = LetterCase.Both,
                    strip_diacritics: bool = False,
                    strip_multigraphs: bool = False,
                    multigraphs_size: MultigraphSize = MultigraphSize.All,
                    as_list: bool = False) -> Union[list[str], dict]:
        """Retrieves characters for a given language based on writing system and filters.

        This function retrieves the characters associated with a specific language. 
        It considers the language's writing system and applies the specified filters.

        Parameters:
            language (Language): The language for which to retrieve characters.
            letter_case (LetterCase, optional): Controls the output letter case 
                (uppercase, lowercase, or both). Defaults to LetterCase.Both.
            strip_diacritics (bool, optional): If True, removes diacritics from the characters. 
                Defaults to False.
            strip_multigraphs (bool, optional): If True, removes multigraphs from the characters 
                based on the specified `multigraphs_size`. Defaults to False.
            multigraphs_size (MultigraphSize, optional): Specifies the size of multigraphs to remove 
                when `strip_multigraphs` is True. Defaults to MultigraphSize.All.
            as_list (bool, optional): If True, returns the characters as a list. Otherwise, returns 
                a dictionary with the language name as the key and the characters as the value. 
                Defaults to False.

        Returns:
            Union[list[str], dict]: A list of characters (if `as_list` is True) or a dictionary 
                mapping the language name to a list of characters (if `as_list` is False).

        Raises:
            ValueError: If the provided language code is not found or an unsupported filter 
                combination is used (e.g., `strip_multigraphs` with Japanese language).

        Special Cases:
            - Languages with multiple writing systems (e.g., Japanese):
                - This function returns a dictionary with each writing system (Hiragana, Katakana, Kanji) 
                as a key and its corresponding characters as a list as a value. 
                - Filters cannot be applied in this case due to the complexity of handling 
                multiple writing systems.
        """
       
        # Check if the accociated language code exists within the internal JsonFile.Alphabet file.
        # If the key is not present, perform a fallback to the other script types contained in the json files and return the respective script.
        alphabet_json = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Alphabet)
        language_code = language.value[0]

        alphabet = None
    
        if language_code not in alphabet_json:
            # Special case for languages that have *multiple* writing systems and non-mapable language codes.
            # ---------------------------------------------------------------------------------------
            # Note that for such languages such as Japanese none of the filters below can be applied. 
            # Also, the parameter *as_list* is ignored, as otherwise it is difficult to understand which list refers to which writing system.
            # Thus, the respective writing system type(s) is/are returned as they are.
            if language == self.Language.Japanese:
                return {self.Language.Japanese.name: {self.Syllabary.Hiragana.name: self.by_syllabary(self.Syllabary.Hiragana, as_list=True),
                        self.Syllabary.Katakana.name : self.by_syllabary(self.Syllabary.Katakana, as_list=True),
                        self.Logographic.Kanji.name : self.by_logographic(self.Logographic.Kanji, as_list=True)}}
            # ---------------------------------------------------------------------------------------

            abjad_dict = dict([(a.name, a.value[0]) for a in self.Abjad])
            abugida_dict = dict([(a.name, a.value[0]) for a in self.Abugida])
            syllabary_dict = dict([(s.name, s.value[0]) for s in self.Syllabary])
            logographic_dict = dict([(l.name, l.value[0]) for l in self.Logographic])
            featural_dict = dict([(l.name, l.value[0]) for l in self.Featural])
            
            # Note: Add other writing systems only when needed..
            for iso_15924_group, languages in self.iso_15924_to_iso_639_2_3.items():
                if language_code in languages:
                    if iso_15924_group in set([a.value[0] for a in self.Abugida]):
                        script = self.by_abugida(self.Abugida[self.retrieve_iso_formal_name(iso_15924_group, self.Abugida)], as_list=True)
                        return script if as_list else {language.name : script}
                    
                    elif iso_15924_group in set([a.value[0] for a in self.Featural]):
                        script = self.by_featural(self.Featural[self.retrieve_iso_formal_name(iso_15924_group, self.Featural)], as_list=True)
                        return script if as_list else {language.name : script}

            if language.name in syllabary_dict:
                script = self.by_syllabary(self.Syllabary[language.name], as_list=True)
                return script if as_list else {language.name : script}

            if language.name in logographic_dict:
                script = self.by_logographic(self.Logographic[language.name], as_list=True)
                return script if as_list else {language.name : script}
            
            if language.name in featural_dict:
                script = self.by_featural(self.Featural[language.name], as_list=True)
                return script if as_list else {language.name : script}

            if language.name in abjad_dict:
                script = self.by_abjad(self.Abjad[language.name], as_list=True)
                return script if as_list else {language.name : script}

            if language.name in abugida_dict:
                script = self.by_abugida(self.Abugida[language.name], as_list=True)
                return script if as_list else {language.name : script}
        else:
            alphabet = alphabet_json[language_code]["script"]

        # In case the given language has an alphabet, the following filters are optional.
        # ---------------------------------------------------------------------------------------
        if strip_diacritics:
            diacritics = set(self.extract_diacritics(alphabet))
            alphabet = [c for c in alphabet if c not in diacritics]

        # Multigraph: https://en.wikipedia.org/wiki/Multigraph_(orthography)
        if strip_multigraphs:
            multigraphs = self.extract_multigraphs(alphabet, multigraphs_size)
            alphabet = [c for c in alphabet if c not in multigraphs]

        if letter_case == self.LetterCase.Lower and self.has_upper_or_lower_case(alphabet):
            alphabet = [c for c in alphabet if c.islower()]

        elif letter_case == self.LetterCase.Upper and self.has_upper_or_lower_case(alphabet):
            alphabet = [c for c in alphabet if c.isupper()]

        return alphabet if as_list else {language.name : alphabet}


    def all_script_characters(self) -> list[str]:
        """
        Retrieve a sorted list of all unique characters used in the scripts of all languages supported by Alphabetic.

        This function aggregates all characters from all available languages by fetching the entire 
        script (alphabet, abjad, ...) for each language using the `by_language` function. 
        The list is then deduplicated and sorted before being returned.

        Returns:
            list[str]: A sorted list of unique characters from all supported language scripts.
        """

        languages = [language for language in self.Language]
        script_characters = list()

        for language in languages:
            # Japanese represents a special case, as here three scripts (Hiragana, Katakana and Kanji) are used
            if language.name == self.Language.Japanese.name:
                jap_scripts = self.by_language(language)["Japanese"]

                for _, chars in jap_scripts.items():
                    script_characters.extend(chars)
            else:
                script_characters.extend(self.by_language(language, as_list=True))

        return sorted(set(script_characters))


    def strip_non_script_characters(self,
                                    input_text: str,
                                    languages: Union[Language, list[Language], None] = None,
                                    process_token_wise: bool = True,
                                    strip_spaces: bool = True) -> str:
        """
            Remove characters from the input string that do not belong to the specified language(s) or script types.

            This function processes the input text to retain only those characters that are part of the script(s) associated 
            with the specified language(s). The function can process the text token-wise (word by word) or as a whole string, 
            and it can also optionally strip spaces from the final result.

            Parameters:
            -----------
            input_text : str
                The text from which non-script characters will be removed.
            
            languages : Language | list[Language] | None, optional
                The language(s) whose script characters are to be retained in the input text. If None, all supported script 
                types will be considered. Defaults to None.
            
            process_token_wise : bool, optional
                If True, the text will be processed token-wise (word by word). If False, the text will be processed as a whole 
                string. Defaults to True.
            
            strip_spaces : bool, optional
                If True, leading and trailing spaces will be stripped from the final result. Defaults to True.

            Returns:
            --------
            str
                The processed text with only the characters belonging to the specified script(s) retained.

            Raises:
            -------
            ValueError
                If the 'languages' argument is not of the expected type (None, Language, or list of Language).

            Examples:
            ---------
            >>> strip_non_script_characters("Hello, こんにちは, Привет!", languages=Language.English)
            'Hello'

            >>> strip_non_script_characters("Schönes클라 Wetter*+/ heute!தமி חדשים", languages=[Language.German, Language.Hebrew])
            'Schönes Wetter heute חדשים'
            """

        # If no language is given, all characters of all supported script types 
        # (abjad, abugida, alphabet, syllabary, logographic and featural) will be used.
        script_characters = []
        
        if languages is None:
            script_characters = self.all_script_characters()
        elif isinstance(languages, self.Language):
            script_characters = self.by_language(languages, as_list=True)
        elif isinstance(languages, list) and all([isinstance(language, self.Language) for language in languages]):
            for language in languages:
                script_characters.extend(self.by_language(language, as_list=True))
        else:
            raise ValueError("Invalid 'languages' argument. Must be one of the following: None|Language|list[Language]")
            
        if process_token_wise:
            result = []
            tokens = input_text.split()
            
            for token in tokens:
                cleaned_token = "".join([c for c in token if c in script_characters])
                result.append(cleaned_token)
            joined = " ".join(result)
        else:
            joined = "".join([c for c in input_text if c in script_characters])
        return joined.strip() if strip_spaces else joined


    def generate_all_characters_in_range(self, unicode_range: str) -> list[str]:
        """
        Generate a list of all characters within a specified Unicode range.

        This function takes a string representing a Unicode range and returns a list
        of characters that fall within this range. The input string should specify
        the range in the format '\\uXXXX-\\uYYYY', where XXXX and YYYY are hexadecimal
        Unicode code points. The function will include both the start and end points
        in the resulting list.

        Parameters:
            unicode_range (str): A string representing the Unicode range in the 
                                format "\\uXXXX-\\uYYYY". For example, "\\u0061-\\u007A"
                                represents the range from 'a' to 'z'.

        Returns:
            list[str]: A list of characters within the specified Unicode range.

        Example:
            >>> generate_all_characters_in_range("\u0061-\u007A")
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        Notes:
            - The function assumes that the input string is properly formatted.
            - The input range is inclusive of both the start and end points.
            - Only one range should be specified in the input string. Multiple ranges
            or individual characters are not supported by this function.
        """

        range_start, range_end = unicode_range.split("-")
        start = ord(range_start)
        end = ord(range_end) + 1  # +1 to include the end character
        return [chr(codepoint) for codepoint in range(start, end)]
