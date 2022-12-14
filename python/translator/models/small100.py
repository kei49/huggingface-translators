from transformers import M2M100ForConditionalGeneration


from python.helpers import get_directory, check_path_exists
from python.translator.model_configs import TranslatorConfig
from python.tokenization_small100 import SMALL100Tokenizer


class SMALL100():
    config: TranslatorConfig
    src_lang: str | None = None
    to_lang: str | None = None
    tokenizer: SMALL100Tokenizer
    model: M2M100ForConditionalGeneration

    def __init__(self, config: TranslatorConfig) -> None:
        self.config = config

        if not check_path_exists(config.model_path):
            self.model = M2M100ForConditionalGeneration.from_pretrained(
                config.pretrained_name)

            self.model.save_pretrained(config.model_path)
        else:
            self.model = M2M100ForConditionalGeneration.from_pretrained(
                config.model_path)

    def set_tokenizer(self, tgt_lang: str) -> None:
        self.tokenizer = SMALL100Tokenizer.from_pretrained(
            self.config.pretrained_name)
        self.tokenizer.tgt_lang = tgt_lang

    def inference(self, inputs: str = None, max_new_tokens: int = 500, num_beams: int = 1):
        inputs = self.tokenizer(inputs, return_tensors="pt")
        generated_tokens = self.model.generate(**inputs,
                                               max_new_tokens=max_new_tokens,)
        outputs = self.tokenizer.batch_decode(
            generated_tokens, skip_special_tokens=True)[0]

        return outputs
