from enum import Enum, auto, IntEnum


class Language(Enum):
    Albanian  = auto(),
    Belarusian = auto(),
    Boko = auto(),
    Bulgarian  = auto(),
    Catalan  = auto(),
    Croatian   = auto(),
    Czech  = auto(),
    Dutch  = auto(),
    English = auto(),
    Finnish  = auto(),
    French = auto(),
    German = auto(),
    Greek = auto(),
    Hawar = auto(),
    Hebrew  = auto(),
    Icelandic  = auto(),
    Italian = auto(),
    Kazakh  = auto(),
    Korean = auto(),
    Kurmanji = auto(),
    Latin  = auto(),
    Latvian   = auto(),
    Lithuanian  = auto(),
    Maltese  = auto(),
    Mongolian = auto(),
    Slovene  = auto(),
    Sorani = auto(),
    Spanish  = auto(),
    Swedish   = auto(),
    Turkish  = auto(),
    Turkmen  = auto()
    

class Alphabet:
    def entire_alphabeth(self, language: Language) -> str:
        alphabeth_dict = {
            Language.Albanian:   "ABCDDhEFGGjHIJKLLlMNNjOPQRRrSShTThUVXXhYZZhabcddhefggjhijklllmnnjopqrrrsshtthuvxxhyzzhÇËçë",
            Language.Belarusian: "ЁІЎАБВГДЕЖЗЙКЛМНОПРСТУФХЦЧШЫЬЭЮЯабвгдежзйклмнопрстуфхцчшыьэюяёіў",
            Language.Boko:       "ABCDEFGHIJKLMNORSShTTsUWYZabcdefghijklmnorsshttsuwyzƁƊƘƙƳƴɗʼ",
            Language.Bulgarian:  "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯабвгдежзийклмнопрстуфхцчшщъьюя", # https://en.wikipedia.org/wiki/Bulgarian_alphabet
            Language.Catalan:    "ABCDEFGHIJKLMNOPQuRSTUVWXYZabcdefghijklmnopqurstuvwxyzÇç", # https://en.wikipedia.org/wiki/Catalan_language
            Language.Croatian:   "ABCDDžEFGHIJKLLjMNNjOPRSTUVZabcddžefghijklljmnnjoprstuvzĆćČĐđŠšŽž", # https://de.wikipedia.org/wiki/Kroatische_Sprache#Alphabet_und_Aussprache
            Language.Czech:      "ABCChDEFGHIJKLMNOPQRSTUVWXYZabcchdefghijklmnopqrstuvwxyzÁÉÍÓÚÝáéíóúýČčĎďĚěŇňŘřŠšŤťŮůŽž",
            Language.Dutch :     "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", # https://en.wikipedia.org/wiki/Dutch_language
            Language.English:    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            Language.Finnish:    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÄÅÖäåö", # https://en.wikipedia.org/wiki/Finnish_orthography
            Language.French:     "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÂÆÇÈÉÊËÎÏÔÙÛÜàâæçèéêëîïôùûüÿŒœŸ",
            Language.German:     "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÄÖÜßäöü",
            Language.Greek:      "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω", # https://en.wikipedia.org/wiki/Greek_alphabet
            Language.Hawar:      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÇÊÎÛçêîûŞş", # https://en.wikipedia.org/wiki/Kurdish_alphabets
            Language.Hebrew:     "ABCDEFGHIJKLMNOPQuRSTUVWXYZabcdefghijklmnopqurstuvwxyzÇç", # https://en.wikipedia.org/wiki/Hebrew_alphabet
            Language.Icelandic:  "ABDEFGHIJKLMNOPRSTUVXYabdefghijklmnoprstuvxyÁÆÉÍÐÓÖÚÝÞáæéíðóöúýþ", # https://en.wikipedia.org/wiki/Icelandic_language
            Language.Italian:    "ABCDEFGHILMNOPQRSTUVZabcdefghilmnopqrstuvz",
            Language.Kazakh:     "ЁІАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёіҒғҚқҢңҮүҰұҺһӘәӨө", # https://en.wikipedia.org/wiki/Kazakh_alphabets
            Language.Korean:     "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ",
            Language.Kurmanji:   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÇÊÎÛçêîûŞş", # https://de.wikipedia.org/wiki/Kurdische_Alphabete
            Language.Latin:      "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", # https://en.wikipedia.org/wiki/Latin_alphabet
            Language.Latvian:    "ABCDEFGHIJKLMNOPRSTUVZabcdefghijklmnoprstuvzĀāČčĒēĢģĪīĶķĻļŅņŠšŪūŽž", # https://en.wikipedia.org/wiki/Latvian_orthography
            Language.Lithuanian: "ABCDEFGHIJKLMNOPRSTUVYZabcdefghijklmnoprstuvyzĄąČčĖėĘęĮįŠšŪūŲųŽž", # https://en.wikipedia.org/wiki/Lithuanian_orthography#Alphabet
            Language.Maltese:    "ABDEFGGĦHIIEJKLMNOPQRSTUVWXZabdefggħhiiejklmnopqrstuvwxzĊċĠġĦħŻż",
            Language.Mongolian:  "ᠠᠡᠢᠣᠤᠥᠦᠨᠪᠫᠬᠬ‍ᠭᠭ‍ᠮᠯᠰᠱᠲᠳᠳ᠊ᠴᠵᠶᠷᠸᠹᠺᠼᠽ",
            Language.Slovene:    "ABCDEFGHIJKLMNOPRSTUVZabcdefghijklmnoprstuvzČčŠšŽž", # https://en.wikipedia.org/wiki/Slovene_alphabet
            Language.Sorani:     "ئـابتجحخدرزسشعغفقلمنوووپچڕژڤکگڵھۆیێە",
            Language.Spanish:    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÑñ",
            Language.Swedish:    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÄÅÖäåö", # https://en.wikipedia.org/wiki/Swedish_language
            Language.Turkish:    "ABCDEFGHIJKLMNOPRSTUVYZabcdefghijklmnoprstuvyzÂÇÎÖÛÜâçîöûüĞğİıŞş",
            Language.Turkmen:    "ABDEFGHIJKLMNOPRSTUWYZabdefghijklmnoprstuwyzÄÇÖÜÝäçöüýŇňŞşŽž",  # Latin, Cyrillic, Arabic; https://en.wikipedia.org/wiki/Turkmen_alphabet,                 
            }

        return alphabeth_dict[language]