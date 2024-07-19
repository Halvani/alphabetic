import os
import sys
import inspect
import unittest
import pytest

# Import the module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from alphabetic import JsonUtils, WritingSystem
from alphabetic.errors import Non_Existing_ISO_639_2_Langcode

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


    def test_iso_code_2_language(self):
        ws = WritingSystem()
        assert (ws.iso_code_to_name("deu") == 'German' and
                ws.iso_code_to_name("Mlym") == 'Malayalam' and
                ws.iso_code_to_name("dng") == 'Dungan')


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
        set("ᎩᎨᏍᏗ").issubset(set(ws.by_syllabary(ws.Syllabary.Cherokee, as_list=True)))


    def test_by_featural(self):
        ws = WritingSystem()
        assert set(['ㅅ','ㅆ','ㅇ','ㅈ',]).issubset(set(ws.by_featural(ws.Featural.Hangul, as_list=True)))


    def test_by_logographic(self):
        ws = WritingSystem()
        assert set(['優','元','兄','充']).issubset(set(ws.by_logographic(ws.Logographic.Kanji, as_list=True)))


    def test_text_to_latin_script_code(self):
        ws = WritingSystem()
        assert ws.text_to_latin_script_code("oren", ws.LatinScriptCode.NATO_Phonetic_Alphabet) == ['Oscar', 'Romeo', 'Echo', 'November']


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


    def test_is_script_type(self):
        ws = WritingSystem()
        # t_i, f_i --> (True, False)
        t0, f0 = ws.is_alphabet(x:="dzień dobry"), ws.is_abjad(x)
        t1, f1 = ws.is_abugida(x:=" ምልካም እድል"), ws.is_logographic(x)
        t2, f2 = ws.is_featural(x:="좋은 아침"), ws.is_syllabary(x)
        t3, f3 = ws.is_abjad(x:="החדשות"), ws.is_abugida(x)
        t4, f4 = ws.is_alphabet(x:=" Nachrichten"), ws.is_featural(x)
        t5, f5 = ws.is_logographic(x:="您好 "), ws.is_featural(x)
        t6, f6 = ws.is_syllabary(x:="ᏧᏂᎸᏫᏍᏓᏁᏗ"), ws.is_featural(x)
        t7, f7 = ws.is_alphabet(x:="Здравейте"), ws.is_abugida(x)
        t8, f8 = ws.is_abjad(x:="مرحبا"), ws.is_logographic(x)
        t9, f9 = ws.is_alphabet(x:="Сәлеметсіз бе"), ws.is_syllabary(x)
        t10, f10 = ws.is_syllabary(x:="こんにちは"), ws.is_alphabet(x)

        assert all([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]) and not any([f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10])


    def test_strip_non_script_characters_single(self):
        ws = WritingSystem()
        assert (ws.strip_non_script_characters("12_-äMil%uji+ jazßyky!öü*~Γpλ\\?/!", ws.Language.Czech) == "Miluji jazykyp" and
                ws.strip_non_script_characters("ΣλI lΟove ΛAlphαabeτtic", ws.Language.English) == "I love Alphabetic" and
                ws.strip_non_script_characters("ΣλI lΟove ΛAlphαabeτtic", ws.Language.Greek) == 'Σλ Ο Λατ' and
                ws.strip_non_script_characters("SΓpλrώaσcσhεeςn!", ws.Language.German) == "Sprachen" and
                ws.strip_non_script_characters("SΓpλrώaσcσhεeςn!", ws.Language.Greek) == "Γλώσσες")
        
        
    def test_strip_non_script_characters_multiple(self):
        ws = WritingSystem()
        assert (ws.strip_non_script_characters("**č,ř,š,ž;Tel ßAviv ÄÖÜתל #אביב++",
                                               [ws.Language.English, ws.Language.Hebrew]) == "Tel Aviv תל אביב" and
                ws.strip_non_script_characters("äöü_-/началник 클라en فجعيةplena 우드ስሉጥtemporadaதமிழ் пожарна",
                                               [ws.Language.Spanish, ws.Language.Bulgarian]) == "началник en plena temporada пожарна")
        

    def test_generate_all_characters_in_range(self):
        ws = WritingSystem()
        
        german_letters_upper = "\u0041-\u005A"
        german_letters_lower = "\u0061-\u007A"
        german_letters_umlauts = "\u00C4\u00D6\u00DC\u00DF\u00E4\u00F6\u00FC"

        upper = ws.generate_all_characters_in_range(german_letters_upper)
        lower = ws.generate_all_characters_in_range(german_letters_lower)
        umlauts = list(german_letters_umlauts.split("\\", maxsplit=1)[0])

        assert "".join(sorted(upper + lower + umlauts)) == "".join(sorted(ws.by_language(ws.Language.German, as_list=True)))
