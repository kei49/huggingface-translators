from enum import Enum, auto
from typing import Dict, Optional
from dataclasses import dataclass, field

from python.helpers import get_directory


class ModelType(Enum):
    MBART_LARGE_50_MANY_TO_MANY = auto()
    MBART_LARGE_50_ONE_TO_MANY = auto()
    MBART_LARGE_50_MANY_TO_ONE = auto()

    SMALL100 = auto()
    M2M100_418M = auto()

    FLAN_T5_BASE = auto()

    MT5_SMALL = auto()
    MT5_BASE = auto()
    # MT5_LARGE = auto()

    ENVIT5_TRANSLATION = auto()
    K024_MT5_ZH_JA_EN_TRIMMED = auto()
    KEN11_MBART_JA_EN = auto()

    OPUS_MT_JA_EN = auto()
    OPUS_MT_EN_JAP = auto()
    OPUS_MT_KO_EN = auto()
    OPUS_MT_TC_BIG_EN_KO = auto()
    OPUS_MT_MUL_EN = auto()


@dataclass
class TranslatorConfig:
    pretrained_name: str
    model_path: str
    available_src_langs: list[str]
    available_tgt_langs: list[str]
    use_gpu: bool = field(init=False)


@dataclass
class TranslateParams:
    model_type: ModelType
    from_la: str
    to_la: str
    src_lang: str = field(init=False)
    tgt_lang: str = field(init=False)


mbart_available_languages = [
    "ar_AR", "cs_CZ" "de_DE", "en_XX", "es_XX" "et_EE", "fi_FI", "fr_XX",
    "gu_IN", "hi_IN", "it_IT", "ja_XX", "kk_KZ", "ko_KR", "lt_LT", "lv_LV",
    "my_MM", "ne_NP", "nl_XX", "ro_RO", "ru_RU" "si_LK", "tr_TR", "vi_VN",
    "zh_CN", "af_ZA", "az_AZ", "bn_IN", "fa_IR", "he_IL", "hr_HR", "id_ID",
    "ka_GE", "km_KH", "mk_MK", "ml_IN", "mn_MN", "mr_IN", "pl_PL", "ps_AF",
    "pt_XX", "sv_SE", "sw_KE", "ta_IN", "te_IN", "th_TH", "tl_XX", "uk_UA",
    "ur_PK", "xh_ZA", "gl_ES", "sl_SI"]

fairseq_available_languages = ["af", "am", "ar", "ast", "az", "ba", "be", "bg", "bn", "br", "bs", "ca", "ceb", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "ff", "fi", "fr", "fy", "ga", "gd", "gl", "gu", "ha", "he", "hi", "hr", "ht", "hu", "hy", "id", "ig", "ilo", "is", "it", "ja", "jv", "ka", "kk", "km",
                               "kn", "ko", "lb", "lg", "ln", "lo", "lt", "lv", "mg", "mk", "ml", "mn", "mr", "ms", "my", "ne", "nl", "no", "ns", "oc", "or", "pa", "pl", "ps", "pt", "ro", "ru", "sd", "si", "sk", "sl", "so", "sq", "sr", "ss", "su", "sv", "sw", "ta", "th", "tl", "tn", "tr", "uk", "ur", "uz", "vi", "wo", "xh", "yi", "yo", "zh", "zu"]

mbart_available_languages_without_en = [
    la for la in mbart_available_languages if la != "en_XX"]

mt5_tmp_availabel_languages = [
    'en', 'ja', 'zh', 'vi', 'ko', 'id'
]

flan_t5_languages = [
    "English", "Spanish", "Japanese", "Persian", "Hindi", "French", "Chinese", "Bengali", "Gujarati", "German", "Telugu", "Italian", "Arabic", "Polish", "Tamil", "Marathi", "Malayalam", "Oriya", "Panjabi", "Portuguese", "Urdu", "Galician", "Hebrew", "Korean", "Catalan", "Thai", "Dutch", "Indonesian", "Vietnamese", "Bulgarian", "Filipino", "CentralKhmer", "Lao", "Turkish", "Russian", "Croatian", "Swedish", "Yoruba", "Kurdish", "Burmese", "Malay", "Czech", "Finnish", "Somali", "Tagalog", "Swahili", "Sinhala", "Kannada", "Zhuang", "Igbo", "Xhosa", "Romanian", "Haitian", "Estonian", "Slovak", "Lithuanian", "Greek", "Nepali", "Assamese", "Norwegian"
]

models = {
    ModelType.OPUS_MT_JA_EN: {
        'name': 'Helsinki-NLP/opus-mt-ko-en',
        'available_src_langs': ['ja'],
        'available_tgt_langs': ['en']
    },
    # ModelType.OPUS_MT_EN_JAP: {
    #     'name': 'Helsinki-NLP/opus-mt-en-jap',
    #     'available_src_langs': ['en'],
    #     'available_tgt_langs': ['jap']
    # },
    ModelType.OPUS_MT_KO_EN: {
        'name': 'Helsinki-NLP/opus-mt-ko-en',
        'available_src_langs': ['ko'],
        'available_tgt_langs': ['en']
    },
    ModelType.OPUS_MT_TC_BIG_EN_KO: {
        'name': 'Helsinki-NLP/opus-mt-tc-big-en-ko',
        'available_src_langs': ['en'],
        'available_tgt_langs': ['ko']
    },
    ModelType.OPUS_MT_MUL_EN: {
        'name': 'Helsinki-NLP/opus-mt-mul-en',
        'available_src_langs': ['ca', 'es', 'os', 'eo', 'ro', 'fy', 'cy', 'is', 'lb', 'su', 'an', 'sq', 'fr',
                                'ht', 'rm', 'cv', 'ig', 'am', 'eu', 'tr', 'ps', 'af', 'ny', 'ch', 'uk', 'sl',
                                'lt', 'tk', 'sg', 'ar', 'lg', 'bg', 'be', 'ka', 'gd', 'ja', 'si', 'br', 'mh', 'km', 'th', 'ty', 'rw', 'te',
                                'mk', 'or', 'wo', 'kl', 'mr', 'ru', 'yo', 'hu', 'fo', 'zh', 'ti', 'co', 'ee', 'oc', 'sn', 'mt', 'ts', 'pl',
                                'gl', 'nb', 'bn', 'tt', 'bo', 'lo', 'id', 'gn', 'nv', 'hy', 'kn', 'to', 'io', 'so', 'vi', 'da', 'fj', 'gv',
                                'sm', 'nl', 'mi', 'pt', 'hi', 'se', 'as', 'ta', 'et', 'kw', 'ga', 'sv', 'ln', 'na', 'mn', 'gu', 'wa', 'lv',
                                'jv', 'el', 'my', 'ba', 'it', 'hr', 'ur', 'ce', 'nn', 'fi', 'mg', 'rn', 'xh', 'ab', 'de', 'cs', 'he', 'zu', 'yi', 'ml', 'mul', 'en'],
        'available_tgt_langs': ['en']
    },
    ModelType.MBART_LARGE_50_MANY_TO_MANY: {
        'name': 'facebook/mbart-large-50-many-to-many-mmt',
        'available_src_langs': mbart_available_languages,
        'available_tgt_langs': mbart_available_languages
    },
    ModelType.MBART_LARGE_50_ONE_TO_MANY: {
        'name': 'facebook/mbart-large-50-one-to-many-mmt',
        'available_src_langs': ['en_XX'],
        'available_tgt_langs': mbart_available_languages_without_en
    },
    ModelType.MBART_LARGE_50_MANY_TO_ONE: {
        'name': 'facebook/mbart-large-50-many-to-one-mmt',
        'available_src_langs': mbart_available_languages_without_en,
        'available_tgt_langs': ['en_XX']
    },
    # ModelType.MT5_SMALL: {
    #     'name': 'google/mt5-small',
    #     'available_src_langs': mt5_tmp_availabel_languages,
    #     'available_tgt_langs': mt5_tmp_availabel_languages
    # },
    # this may require gpu
    # ModelType.MT5_BASE: {
    #     'name': 'google/mt5-base',
    #     'available_src_langs': mt5_tmp_availabel_languages,
    #     'available_tgt_langs': mt5_tmp_availabel_languages
    # },
    ModelType.ENVIT5_TRANSLATION: {
        'name': 'VietAI/envit5-translation',
        'available_src_langs': ['vi', 'en'],
        'available_tgt_langs': ['vi', 'en']
    },
    ModelType.K024_MT5_ZH_JA_EN_TRIMMED: {
        'name': 'K024/mt5-zh-ja-en-trimmed',
        'available_src_langs': ['zh', 'ja', 'en'],
        'available_tgt_langs': ['zh', 'ja', 'en']
    },
    ModelType.KEN11_MBART_JA_EN: {
        'name': 'ken11/mbart-ja-en',
        'available_src_langs': ['ja'],
        'available_tgt_langs': ['en']
    },
    ModelType.SMALL100: {
        'name': 'alirezamsh/small100',
        'available_src_langs': fairseq_available_languages,
        'available_tgt_langs': fairseq_available_languages
    },
    # ModelType.M2M100_418M: {
    #     'name': 'facebook/m2m100_418M',
    #     'available_src_langs': fairseq_available_languages,
    #     'available_tgt_langs': fairseq_available_languages
    # },
    # ModelType.FLAN_T5_BASE: {
    #     'name': 'google/flan-t5-base',
    #     'available_src_langs': flan_t5_languages,
    #     'available_tgt_langs': flan_t5_languages
    # }
}


def get_translator_config(model_type: ModelType):
    def get_model_path(name: str):
        return get_directory(name.replace('/', '_'))

    def generate_translator_config(d: Dict):
        return TranslatorConfig(d['name'], get_model_path(d['name']), d['available_src_langs'], d['available_tgt_langs'])

    return generate_translator_config(models[model_type])


def get_all_available_models(from_la: str, to_la: str):
    available_models: list[TranslateParams] = []

    for model_type, value in models.items():
        src_langs = [
            lang for lang in value['available_src_langs'] if from_la in lang]
        tgt_langs = [
            lang for lang in value['available_tgt_langs'] if to_la in lang]

        if len(src_langs) > 0 and len(tgt_langs) > 0:
            t_p = TranslateParams(
                model_type, from_la, to_la)
            t_p.src_lang = src_langs[0]
            t_p.tgt_lang = tgt_langs[0]

            available_models.append(t_p)

    return available_models
