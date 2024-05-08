import dcl
import json
from pathlib import Path
from enum import Enum, auto

from .errors import *

# Notes: 
# -------------------------------
# Clarify --> Hawar (Language?):   ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "Ç", "Ê", "Î", "Û", "ç", "ê", "î", "û", "Ş", "ş"], # https://en.wikipedia.org/wiki/Kurdish_alphabets
# Clarify --> Mahajani (Language?): ["𑅐", "𑅑", "𑅒", "𑅓", "𑅔", "𑅕", "𑅖", "𑅗", "𑅘", "𑅙", "𑅚", "𑅛", "𑅜", "𑅝", "𑅞", "𑅟", "𑅠", "𑅡", "𑅢", "𑅣", "𑅤", "𑅥", "𑅦", "𑅧", "𑅨", "𑅩", "𑅪", "𑅫", "𑅬", "𑅭", "𑅮", "𑅯", "𑅰", "𑅱", "𑅲"],  What is the language code? --> https://en.wikipedia.org/wiki/Mahajani 

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
           
class LetterCase(Enum):
    Lower = auto(),
    Upper = auto(),
    Both = auto()


class Code(Enum):
    Morse = auto(),
    NATO_Phonetic_Alphabet = auto(),


class Language(Enum):
    # According to: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes

    Albanian = "sqi",
    Assamese = "asm",
    Amharic = "amh",
    Bambara = "bam",
    Basque = "baq",
    Afrikaans = "afr",
    Arabic = "ara",
    Bashkir = "bak",
    Belarusian = "bel",
    Boko = "bqc",
    Bosnian = "bos",
    Bulgarian = "bul",
    Buryat = "bua", 
    Catalan = "cat",
    Chechen = "che",
    Cherokee = "chr", 
    Chukchi = "ckt",
    Croatian = "hrv",
    Czech = "ces",
    Danish = "dan",
    Dungan = "dng",
    Dutch = "nld",
    English = "eng",
    Esperanto = "epo",
    Estonian = "est",
    Finnish = "fin",
    French = "fra",
    Georgian = "kat",
    German = "deu",
    Corsican = "cos",
    Greek = "gre",
    Hawaiian = "haw",
    Hebrew = "heb",
    Icelandic = "isl",
    Indonesian = "ind",
    Italian = "ita",
    Javanese = "jav",
    Kashubian = "csb",
    Kazakh = "kaz",
    Kirghiz = "kir",    # aka Kyrgyz
    Korean = "kor",
    Kumyk = "kum",
    Kurmanji = "kmr",   
    Latin = "lat",
    Latvian = "lav",
    Lezghian = "lez",
    Lithuanian = "lit",
    Macedonian = "mkd",
    Maltese = "mlt",
    Malay = "may",
    Maori = "mao",
    Mari = "chm",
    Moldovan  = "rum",
    Mongolian = "mon",
    Mru = "mro",
    Nepali  = "nep",
    Norwegian  = "nor",
    Occitan = "oci",
    Pashto = "pus",
    Persian = "per",
    Polish = "pol",
    Portuguese = "por",
    Punjabi = "pan",
    Rohingya  = "rhg",
    Romanian = "rum",
    Russian = "rus",
    Sango = "sag",
    Sanskrit = "san",
    Serbian = "srp",
    Slovak = "slo",
    Slovenian = "slv", # aka Slovene
    Somali = "som",
    Samoan  = "smo",
    Sorani = "ckb", 
    Spanish = "spa",
    Sundanese = "sun",
    Swedish = "swe",
    Tajik  = "tgk",
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
    Quechua  = "que",
    Hindi = "hin",

    
    
        

class Syllabary:
    pass
    # Hiragana = ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と", "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ", "ま", "み", "む", "め", "も", "や", "ゆ", "よ", "ら", "り", "る", "れ", "ろ", "わ", "を", "ん"], 

    # Katakana = ["ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", "ト", "ナ", "ニ", "ヌ", "ネ", "ノ", "ハ", "ヒ", "フ", "ヘ", "ホ", "マ", "ミ", "ム", "メ", "モ", "ヤ", "ユ", "ヨ", "ラ", "リ", "ル", "レ", "ロ", "ワ", "ヲ", "ン"], 

    #Cherokee = ["Ꭰ", "Ꭱ", "Ꭲ", "Ꭳ", "Ꭴ", "Ꭵ", "Ꭶ", "Ꭷ", "Ꭸ", "Ꭹ", "Ꭺ", "Ꭻ", "Ꭼ", "Ꭽ", "Ꭾ", "Ꭿ", "Ꮀ", "Ꮁ", "Ꮂ", "Ꮃ", "Ꮄ", "Ꮅ", "Ꮆ", "Ꮇ", "Ꮈ", "Ꮉ", "Ꮊ", "Ꮋ", "Ꮌ", "Ꮍ", "Ꮎ", "Ꮏ", "Ꮐ", "Ꮑ", "Ꮒ", "Ꮓ", "Ꮔ", "Ꮕ", "Ꮖ", "Ꮗ", "Ꮘ", "Ꮙ", "Ꮚ", "Ꮛ", "Ꮜ", "Ꮝ", "Ꮞ", "Ꮟ", "Ꮠ", "Ꮡ", "Ꮢ", "Ꮣ", "Ꮤ", "Ꮥ", "Ꮦ", "Ꮧ", "Ꮨ", "Ꮩ", "Ꮪ(du),", "Ꮫ", "Ꮬ", "Ꮭ", "Ꮮ", "Ꮯ", "Ꮰ", "Ꮱ", "Ꮲ", "Ꮳ", "Ꮴ", "Ꮵ", "Ꮶ", "Ꮷ", "Ꮸ", "Ꮹ", "Ꮺ", "Ꮻ", "Ꮼ", "Ꮽ", "Ꮾ", "Ꮿ", "Ᏸ", "Ᏹ", "Ᏺ", "Ᏻ", "Ᏼ", "Ᏽ"],
   


class Logographic:
    # Kanji = ["一", "丁", "七", "万", "丈", "三", "上", "下", "不", "与", "且", "世", "丘", "丙", "両", "並", "中", "串", "丸", "丹", "主", "丼", "久", "乏", "乗", "乙", "九", "乞", "乱", "乳", "乾", "亀", "了", "予", "争", "事", "二", "互", "五", "井", "亜", "亡", "交", "享", "京", "亭", "人", "仁", "今", "介", "仏", "仕", "他", "付", "仙", "代", "令", "以", "仮", "仰", "仲", "件", "任", "企", "伎", "伏", "伐", "休", "会", "伝", "伯", "伴", "伸", "伺", "似", "但", "位", "低", "住", "佐", "体", "何", "余", "作", "佳", "併", "使", "例", "侍", "供", "依", "価", "侮", "侯", "侵", "侶", "便", "係", "促", "俊", "俗", "保", "信", "修", "俳", "俵", "俸", "俺", "倉", "個", "倍", "倒", "候", "借", "倣", "値", "倫", "倹", "偉", "偏", "停", "健", "側", "偵", "偶", "偽", "傍", "傑", "傘", "備", "催", "傲", "債", "傷", "傾", "僅", "働", "像", "僕", "僚", "僧", "儀", "億", "儒", "償", "優", "元", "兄", "充", "兆", "先", "光", "克", "免", "児", "党", "入", "全", "八", "公", "六", "共", "兵", "具", "典", "兼", "内", "円", "冊", "再", "冒", "冗", "写", "冠", "冥", "冬", "冶", "冷", "凄", "准", "凍", "凝", "凡", "処", "凶", "凸", "凹", "出", "刀", "刃", "分", "切", "刈", "刊", "刑", "列", "初", "判", "別", "利", "到", "制", "刷", "券", "刹", "刺", "刻", "則", "削", "前", "剖", "剛", "剝", "剣", "剤", "副", "剰", "割", "創", "劇", "力", "功", "加", "劣", "助", "努", "励", "労", "効", "劾", "勃", "勅", "勇", "勉", "動", "勘", "務", "勝", "募", "勢", "勤", "勧", "勲", "勾", "匂", "包", "化", "北", "匠", "匹", "区", "医", "匿", "十", "千", "升", "午", "半", "卑", "卒", "卓", "協", "南", "単", "博", "占", "印", "危", "即", "却", "卵", "卸", "厄", "厘", "厚", "原", "厳", "去", "参", "又", "及", "友", "双", "反", "収", "叔", "取", "受", "叙", "口", "古", "句", "叫", "召", "可", "台", "史", "右", "号", "司", "各", "合", "吉", "同", "名", "后", "吏", "吐", "向", "君", "吟", "否", "含", "吸", "吹", "呂", "呈", "呉", "告", "周", "呪", "味", "呼", "命", "和", "咲", "咽", "哀", "品", "員", "哲", "哺", "唄", "唆", "唇", "唐", "唯", "唱", "唾", "商", "問", "啓", "善", "喉", "喚", "喜", "喝", "喩", "喪", "喫", "営", "嗅", "嗣", "嘆", "嘱", "嘲", "器", "噴", "嚇", "囚", "四", "回", "因", "団", "困", "囲", "図", "固", "国", "圏", "園", "土", "圧", "在", "地", "坂", "均", "坊", "坑", "坪", "垂", "型", "垣", "埋", "城", "域", "執", "培", "基", "埼", "堀", "堂", "堅", "堆", "堕", "堤", "堪", "報", "場", "塀", "塁", "塊", "塑", "塔", "塗", "塚", "塞", "塡", "塩", "塾", "境", "墓", "増", "墜", "墨", "墳", "墾", "壁", "壇", "壊", "壌", "士", "壮", "声", "壱", "売", "変", "夏", "夕", "外", "多", "夜", "夢", "大", "天", "太", "夫", "央", "失", "奇", "奈", "奉", "奏", "契", "奔", "奥", "奨", "奪", "奮", "女", "奴", "好", "如", "妃", "妄", "妊", "妖", "妙", "妥", "妨", "妬", "妹", "妻", "姉", "始", "姓", "委", "姫", "姻", "姿", "威", "娘", "娠", "娯", "婆", "婚", "婦", "婿", "媒", "媛", "嫁", "嫉", "嫌", "嫡", "嬢", "子", "孔", "字", "存", "孝", "季", "孤", "学", "孫", "宅", "宇", "守", "安", "完", "宗", "官", "宙", "定", "宛", "宜", "宝", "実", "客", "宣", "室", "宮", "宰", "害", "宴", "宵", "家", "容", "宿", "寂", "寄", "密", "富", "寒", "寛", "寝", "察", "寡", "寧", "審", "寮", "寸", "寺", "対", "寿", "封", "専", "射", "将", "尉", "尊", "尋", "導", "小", "少", "尚", "就", "尺", "尻", "尼", "尽", "尾", "尿", "局", "居", "屈", "届", "屋", "展", "属", "層", "履", "屯", "山", "岐", "岡", "岩", "岬", "岳", "岸", "峠", "峡", "峰", "島", "崇", "崎", "崖", "崩", "嵐", "川", "州", "巡", "巣", "工", "左", "巧", "巨", "差", "己", "巻", "巾", "市", "布", "帆", "希", "帝", "帥", "師", "席", "帯", "帰", "帳", "常", "帽", "幅", "幕", "幣", "干", "平", "年", "幸", "幹", "幻", "幼", "幽", "幾", "庁", "広", "床", "序", "底", "店", "府", "度", "座", "庫", "庭", "庶", "康", "庸", "廃", "廉", "廊", "延", "廷", "建", "弁", "弄", "弊", "式", "弐", "弓", "弔", "引", "弟", "弥", "弦", "弧", "弱", "張", "強", "弾", "当", "彙", "形", "彩", "彫", "彰", "影", "役", "彼", "往", "征", "径", "待", "律", "後", "徐", "徒", "従", "得", "御", "復", "循", "微", "徳", "徴", "徹", "心", "必", "忌", "忍", "志", "忘", "忙", "応", "忠", "快", "念", "怒", "怖", "思", "怠", "急", "性", "怨", "怪", "恋", "恐", "恒", "恣", "恥", "恨", "恩", "恭", "息", "恵", "悔", "悟", "悠", "患", "悦", "悩", "悪", "悲", "悼", "情", "惑", "惜", "惧", "惨", "惰", "想", "愁", "愉", "意", "愚", "愛", "感", "慄", "慈", "態", "慌", "慎", "慕", "慢", "慣", "慨", "慮", "慰", "慶", "憂", "憎", "憤", "憧", "憩", "憬", "憲", "憶", "憾", "懇", "懐", "懲", "懸", "成", "我", "戒", "戚", "戦", "戯", "戴", "戸", "戻", "房", "所", "扇", "扉", "手", "才", "打", "払", "扱", "扶", "批", "承", "技", "抄", "把", "抑", "投", "抗", "折", "抜", "択", "披", "抱", "抵", "抹", "押", "抽", "担", "拉", "拍", "拐", "拒", "拓", "拘", "拙", "招", "拝", "拠", "拡", "括", "拭", "拳", "拶", "拷", "拾", "持", "指", "挑", "挙", "挟", "挨", "挫", "振", "挿", "捉", "捕", "捗", "捜", "捨", "据", "捻", "掃", "授", "掌", "排", "掘", "掛", "採", "探", "接", "控", "推", "措", "掲", "描", "提", "揚", "換", "握", "揮", "援", "揺", "損", "搬", "搭", "携", "搾", "摂", "摘", "摩", "摯", "撃", "撤", "撮", "撲", "擁", "操", "擦", "擬", "支", "改", "攻", "放", "政", "故", "敏", "救", "敗", "教", "敢", "散", "敬", "数", "整", "敵", "敷", "文", "斉", "斎", "斑", "斗", "料", "斜", "斤", "斥", "斬", "断", "新", "方", "施", "旅", "旋", "族", "旗", "既", "日", "旦", "旧", "旨", "早", "旬", "旺", "昆", "昇", "明", "易", "昔", "星", "映", "春", "昧", "昨", "昭", "是", "昼", "時", "晩", "普", "景", "晴", "晶", "暁", "暇", "暑", "暖", "暗", "暦", "暫", "暮", "暴", "曇", "曖", "曜", "曲", "更", "書", "曹", "曽", "替", "最", "月", "有", "服", "朕", "朗", "望", "朝", "期", "木", "未", "末", "本", "札", "朱", "朴", "机", "朽", "杉", "材", "村", "束", "条", "来", "杯", "東", "松", "板", "析", "枕", "林", "枚", "果", "枝", "枠", "枢", "枯", "架", "柄", "某", "染", "柔", "柱", "柳", "柵", "査", "柿", "栃", "栄", "栓", "校", "株", "核", "根", "格", "栽", "桁", "桃", "案", "桑", "桜", "桟", "梅", "梗", "梨", "械", "棄", "棋", "棒", "棚", "棟", "森", "棺", "椅", "植", "椎", "検", "業", "極", "楷", "楼", "楽", "概", "構", "様", "槽", "標", "模", "権", "横", "樹", "橋", "機", "欄", "欠", "次", "欧", "欲", "欺", "款", "歌", "歓", "止", "正", "武", "歩", "歯", "歳", "歴", "死", "殉", "殊", "残", "殖", "殴", "段", "殺", "殻", "殿", "毀", "母", "毎", "毒", "比", "毛", "氏", "民", "気", "水", "氷", "永", "氾", "汁", "求", "汎", "汗", "汚", "江", "池", "汰", "決", "汽", "沃", "沈", "沖", "沙", "没", "沢", "河", "沸", "油", "治", "沼", "沿", "況", "泉", "泊", "泌", "法", "泡", "波", "泣", "泥", "注", "泰", "泳", "洋", "洗", "洞", "津", "洪", "活", "派", "流", "浄", "浅", "浜", "浦", "浪", "浮", "浴", "海", "浸", "消", "涙", "涯", "液", "涼", "淑", "淡", "淫", "深", "混", "添", "清", "渇", "済", "渉", "渋", "渓", "減", "渡", "渦", "温", "測", "港", "湖", "湧", "湯", "湾", "湿", "満", "源", "準", "溝", "溶", "溺", "滅", "滋", "滑", "滝", "滞", "滴", "漁", "漂", "漆", "漏", "演", "漠", "漢", "漫", "漬", "漸", "潔", "潜", "潟", "潤", "潮", "潰", "澄", "激", "濁", "濃", "濫", "濯", "瀬", "火", "灯", "灰", "災", "炉", "炊", "炎", "炭", "点", "為", "烈", "無", "焦", "然", "焼", "煎", "煙", "照", "煩", "煮", "熊", "熟", "熱", "燃", "燥", "爆", "爪", "爵", "父", "爽", "片", "版", "牙", "牛", "牧", "物", "牲", "特", "犠", "犬", "犯", "状", "狂", "狙", "狩", "独", "狭", "猛", "猟", "猫", "献", "猶", "猿", "獄", "獣", "獲", "玄", "率", "玉", "王", "玩", "珍", "珠", "班", "現", "球", "理", "琴", "瑠", "璃", "璧", "環", "璽", "瓦", "瓶", "甘", "甚", "生", "産", "用", "田", "由", "甲", "申", "男", "町", "画", "界", "畏", "畑", "畔", "留", "畜", "畝", "略", "番", "異", "畳", "畿", "疎", "疑", "疫", "疲", "疾", "病", "症", "痕", "痘", "痛", "痢", "痩", "痴", "瘍", "療", "癒", "癖", "発", "登", "白", "百", "的", "皆", "皇", "皮", "皿", "盆", "益", "盗", "盛", "盟", "監", "盤", "目", "盲", "直", "相", "盾", "省", "眉", "看", "県", "真", "眠", "眺", "眼", "着", "睡", "督", "睦", "瞬", "瞭", "瞳", "矛", "矢", "知", "短", "矯", "石", "砂", "研", "砕", "砲", "破", "硝", "硫", "硬", "碁", "碑", "確", "磁", "磨", "礁", "礎", "示", "礼", "社", "祈", "祉", "祖", "祝", "神", "祥", "票", "祭", "禁", "禅", "禍", "福", "秀", "私", "秋", "科", "秒", "秘", "租", "秩", "称", "移", "程", "税", "稚", "種", "稲", "稼", "稽", "稿", "穀", "穂", "積", "穏", "穫", "穴", "究", "空", "突", "窃", "窒", "窓", "窟", "窮", "窯", "立", "竜", "章", "童", "端", "競", "竹", "笑", "笛", "符", "第", "筆", "等", "筋", "筒", "答", "策", "箇", "箋", "算", "管", "箱", "箸", "節", "範", "築", "篤", "簡", "簿", "籍", "籠", "米", "粉", "粋", "粒", "粗", "粘", "粛", "粧", "精", "糖", "糧", "糸", "系", "糾", "紀", "約", "紅", "紋", "納", "純", "紙", "級", "紛", "素", "紡", "索", "紫", "累", "細", "紳", "紹", "紺", "終", "組", "経", "結", "絞", "絡", "給", "統", "絵", "絶", "絹", "継", "続", "維", "綱", "網", "綻", "綿", "緊", "総", "緑", "緒", "線", "締", "編", "緩", "緯", "練", "緻", "縁", "縄", "縛", "縦", "縫", "縮", "績", "繁", "繊", "織", "繕", "繭", "繰", "缶", "罪", "置", "罰", "署", "罵", "罷", "羅", "羊", "美", "羞", "群", "羨", "義", "羽", "翁", "翌", "習", "翻", "翼", "老", "考", "者", "耐", "耕", "耗", "耳", "聖", "聞", "聴", "職", "肉", "肌", "肖", "肘", "肝", "股", "肢", "肥", "肩", "肪", "肯", "育", "肺", "胃", "胆", "背", "胎", "胞", "胴", "胸", "能", "脂", "脅", "脇", "脈", "脊", "脚", "脱", "脳", "腎", "腐", "腕", "腫", "腰", "腸", "腹", "腺", "膚", "膜", "膝", "膨", "膳", "臆", "臓", "臣", "臨", "自", "臭", "至", "致", "臼", "興", "舌", "舎", "舗", "舞", "舟", "航", "般", "舶", "舷", "船", "艇", "艦", "良", "色", "艶", "芋", "芝", "芯", "花", "芳", "芸", "芽", "苗", "苛", "若", "苦", "英", "茂", "茎", "茨", "茶", "草", "荒", "荘", "荷", "菊", "菌", "菓", "菜", "華", "萎", "落", "葉", "著", "葛", "葬", "蒸", "蓄", "蓋", "蔑", "蔵", "蔽", "薄", "薦", "薪", "薫", "薬", "藍", "藤", "藩", "藻", "虎", "虐", "虚", "虜", "虞", "虫", "虹", "蚊", "蚕", "蛇", "蛍", "蛮", "蜂", "蜜", "融", "血", "衆", "行", "術", "街", "衛", "衝", "衡", "衣", "表", "衰", "衷", "袋", "袖", "被", "裁", "裂", "装", "裏", "裕", "補", "裸", "製", "裾", "複", "褐", "褒", "襟", "襲", "西", "要", "覆", "覇", "見", "規", "視", "覚", "覧", "親", "観", "角", "解", "触", "言", "訂", "訃", "計", "討", "訓", "託", "記", "訟", "訪", "設", "許", "訳", "訴", "診", "証", "詐", "詔", "評", "詞", "詠", "詣", "試", "詩", "詮", "詰", "話", "該", "詳", "誇", "誉", "誌", "認", "誓", "誕", "誘", "語", "誠", "誤", "説", "読", "誰", "課", "調", "談", "請", "論", "諦", "諧", "諭", "諮", "諸", "諾", "謀", "謁", "謄", "謎", "謙", "講", "謝", "謡", "謹", "識", "譜", "警", "議", "譲", "護", "谷", "豆", "豊", "豚", "象", "豪", "貌", "貝", "貞", "負", "財", "貢", "貧", "貨", "販", "貪", "貫", "責", "貯", "貴", "買", "貸", "費", "貼", "貿", "賀", "賂", "賃", "賄", "資", "賊", "賓", "賛", "賜", "賞", "賠", "賢", "賦", "質", "賭", "購", "贈", "赤", "赦", "走", "赴", "起", "超", "越", "趣", "足", "距", "跡", "路", "跳", "践", "踊", "踏", "踪", "蹴", "躍", "身", "車", "軌", "軍", "軒", "軟", "転", "軸", "軽", "較", "載", "輝", "輩", "輪", "輸", "轄", "辛", "辞", "辣", "辱", "農", "辺", "込", "迅", "迎", "近", "返", "迫", "迭", "述", "迷", "追", "退", "送", "逃", "逆", "透", "逐", "逓", "途", "通", "逝", "速", "造", "連", "逮", "週", "進", "逸", "遂", "遅", "遇", "遊", "運", "遍", "過", "道", "達", "違", "遜", "遠", "遡", "遣", "適", "遭", "遮", "遵", "遷", "選", "遺", "避", "還", "那", "邦", "邪", "邸", "郊", "郎", "郡", "部", "郭", "郵", "郷", "都", "酌", "配", "酎", "酒", "酔", "酢", "酪", "酬", "酵", "酷", "酸", "醒", "醜", "醸", "采", "釈", "里", "重", "野", "量", "金", "釜", "針", "釣", "鈍", "鈴", "鉄", "鉛", "鉢", "鉱", "銀", "銃", "銅", "銘", "銭", "鋭", "鋳", "鋼", "錠", "錦", "錬", "錮", "錯", "録", "鍋", "鍛", "鍵", "鎌", "鎖", "鎮", "鏡", "鐘", "鑑", "長", "門", "閉", "開", "閑", "間", "関", "閣", "閥", "閲", "闇", "闘", "阜", "阪", "防", "阻", "附", "降", "限", "陛", "院", "陣", "除", "陥", "陪", "陰", "陳", "陵", "陶", "陸", "険", "陽", "隅", "隆", "隊", "階", "随", "隔", "隙", "際", "障", "隠", "隣", "隷", "隻", "雄", "雅", "集", "雇", "雌", "雑", "離", "難", "雨", "雪", "雰", "雲", "零", "雷", "電", "需", "震", "霊", "霜", "霧", "露", "青", "静", "非", "面", "革", "靴", "韓", "音", "韻", "響", "頂", "頃", "項", "順", "須", "預", "頑", "頒", "頓", "領", "頭", "頰", "頻", "頼", "題", "額", "顎", "顔", "顕", "願", "類", "顧", "風", "飛", "食", "飢", "飯", "飲", "飼", "飽", "飾", "餅", "養", "餌", "餓", "館", "首", "香", "馬", "駄", "駅", "駆", "駐", "駒", "騎", "騒", "験", "騰", "驚", "骨", "骸", "髄", "高", "髪", "鬱", "鬼", "魂", "魅", "魔", "魚", "鮮", "鯨", "鳥", "鳴", "鶏", "鶴", "鹿", "麓", "麗", "麦", "麺", "麻", "黄", "黒", "黙", "鼓", "鼻", "齢", "𠮟"],
    pass   


class Alphabet:

    @staticmethod
    def update_lang_json_file(langcode: str, 
                              alphabet: list[str], 
                              json_filename=r"alphabetic/data/language_data.json") -> None:
        
        json_data = Path(json_filename).read_text(encoding="utf8")
        alphabet_dict = json.loads(json_data)

        alphabet_dict[langcode] = {"alphabet": alphabet}

        Path(json_filename).write_text(json.dumps(alphabet_dict))

        created_dict = json.loads(Path(json_data).read_text(encoding="utf8"))
        if langcode in created_dict:
            print(f"Updated json-file successfully! Alphabet size: {len(created_dict)} (characters).")    
        else:
            print("Something went wrong. Json file could not be written.")  



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
                    only_true_alphabet: bool = False,
                    strip_diphthongs: bool = False,
                    json_filename=r"alphabetic/data/language_data.json") -> str:  


        if not Path(json_filename).exists():
            raise FileNotFoundError(f"Internal json file: [{json_filename}] could not be found. This file contains all supported language alphabets.")
        
        json_data = Path(json_filename).read_text(encoding="utf8")
        alphabet_dict = json.loads(json_data)
        langcode = language.value[0]

        alphabet = alphabet_dict[langcode]["alphabet"]


        if only_true_alphabet:
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



