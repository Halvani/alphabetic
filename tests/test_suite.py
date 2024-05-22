import os
import sys
import pytest
import inspect
import unittest

# Import the module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from alphabetic import JsonUtils, WritingSystem
from alphabetic.errors import *

class TestCore(unittest.TestCase):

    def test_json_files_presence(self):
        try:
            WritingSystem()
        except FileNotFoundError:
            pytest.fail("FileNotFoundError --> Json files not present!")


    def test_update_jsonfile_invalid_iso_639_2_langcode(self):
        with pytest.raises(Non_Existing_ISO_639_2_Langcode):
            JsonUtils.update_lang_json_file("xxx", ["x", "y", "z"])


    def test_delete_non_existing_key_from_jsonfile(self):
        with pytest.raises(Non_Existing_ISO_639_2_Langcode):
            JsonUtils.del_entry_from_jsonfile(JsonUtils.FilePath.Abjad, "xxx")


    # Ensure we first delete the entry, and later add it again to the json file.
    #-------------------------------------------------------------------------
    def test_delete_entry_from_jsonfile(self):
        langcode = "haw"
        JsonUtils.del_entry_from_jsonfile(JsonUtils.FilePath.Alphabet, "haw")
        dict_ = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Alphabet)
        assert langcode not in dict_

    def test_update_jsonfile(self):
        langcode, alphabet = "haw", ["A", "E", "H", "I", "K", "L", "M", "N", "O", "P", "U", "W", "a", "e", "h", "i", "k", "l", "m", "n", "o", "p", "u", "w", "ʻ"] 
        JsonUtils.update_lang_json_file(langcode, alphabet)
        dict_ = JsonUtils.load_dict_from_jsonfile(JsonUtils.FilePath.Alphabet)
        assert langcode in dict_ and sorted(dict_[langcode]["script"]) == sorted(alphabet)
    #-------------------------------------------------------------------------

    def test_diacritics_handling(self):
        ws = WritingSystem()
        german_alphabet = ws.by_language(ws.Language.German, as_list=True)
        diacritics = ws.extract_diacritics(german_alphabet)
        assert set(diacritics).issubset(set(german_alphabet))


    def test_strip_multigraphs(self):
        ws = WritingSystem()
        X = ws.by_language(ws.Language.Aleut, strip_multigraphs=True, multigraphs_size=ws.MultigraphSize.All, as_list=True)
        assert any([len(x) == 1 for x in X])


    def test_valid_lower_upper_case_extraction(self):
        ws = WritingSystem()
        bosnian_lower_alphabet = ws.by_language(ws.Language.Bosnian, letter_case=ws.LetterCase.Lower, as_list=True)
        assert all([a.islower() for a in bosnian_lower_alphabet])


    def test_invalid_lower_upper_case_extraction(self):
        ws = WritingSystem()
        hebrew_alphabet = ws.by_language(x:=ws.Language.Hebrew, as_list=True)
        assert (ws.by_language(x, letter_case=ws.LetterCase.Lower)[x.name] == hebrew_alphabet 
                and ws.by_language(x, letter_case=ws.LetterCase.Upper)[x.name] == hebrew_alphabet)
         

    def test_fallback_strategy(self):
        ws = WritingSystem()
        chinese_simplified_alphabet = ws.by_language(ws.Language.Chinese_Simplified, as_list=True)
        assert len(chinese_simplified_alphabet) == len(ws.by_logographic(ws.Logographic.Chinese_Simplified, as_list=True))


    def test_by_abjad(self):
        ws = WritingSystem()
        assert set(['𐤉','𐤊','𐤋']).issubset(set(ws.by_abjad(ws.Abjad.Phoenician, as_list=True)))


    def test_by_abugida(self):
        ws = WritingSystem()
        assert set(['ङ','च','छ','ज']).issubset(set(ws.by_abugida(ws.Abugida.Devanagari, as_list=True)))


    def test_by_syllabary(self):
        ws = WritingSystem()
        assert set(['ዟ','የ','ዩ','ዪ']).issubset(set(ws.by_syllabary(ws.Syllabary.Ethiopic, as_list=True)))


    def test_by_featural(self):
        ws = WritingSystem()
        assert set(['ㅅ','ㅆ','ㅇ','ㅈ',]).issubset(set(ws.by_featural(ws.Featural.Hangul, as_list=True)))


    def test_by_logographic(self):
        ws = WritingSystem()
        assert set(['優','元','兄','充']).issubset(set(ws.by_logographic(ws.Logographic.Kanji, as_list=True)))


    def test_by_code(self):
        ws = WritingSystem()
        alphabet = ws.by_code(ws.LatinScriptCode.NATO_Phonetic_Alphabet)
        assert [alphabet[c] for c in "HALVANI"] == ['Hotel', 'Alfa', 'Lima', 'Victor', 'Alfa', 'November', 'India']


    def test_iso_15924_maps_to_iso_639_test_1(self):
        with pytest.raises(ValueError):
            ws = WritingSystem()
            ws.retrieve_iso_formal_name("xxxx", ws.Syllabary)


    def test_iso_15924_maps_to_iso_639_test_2(self):
        ws = WritingSystem()
        assert sorted(ws.by_language(ws.Language.Jeju, as_list=True)) == sorted(ws.by_language(ws.Language.Korean, as_list=True))


    def test_multiple_writing_systems(self):
        ws = WritingSystem()
        assert sorted(ws.by_language(x:=ws.Language.Japanese)[x.name].keys()) == ['Hiragana', 'Kanji', 'Katakana']