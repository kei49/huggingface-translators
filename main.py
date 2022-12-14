import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from python.translator.model_configs import get_all_available_models
from python.translator.manager import Manager, ModelType, TranslateParams
from python.timer import Timer
from python.logger import use_logger
logger = use_logger(__name__)


app = FastAPI()

origins = [
    "*"
    # "https://translators-ui.web.app/",
    # "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslateRequestParams(BaseModel):
    texts: str
    from_la: str
    to_la: str


manager = Manager()


@app.get("/")
def health_check():
    logger.info(f"{os.getpid()} worker is handling the request")
    return {"message": "Hello World"}


@app.post("/translate/all")
def translate_all(req: TranslateRequestParams):
    logger.info(f"{os.getpid()} worker is handling the request")

    available_models_t_p = get_all_available_models(req.from_la, req.to_la)

    logger.info(f"{available_models_t_p=}")

    all_outputs = []

    for t_p in available_models_t_p:
        try:
            with Timer(logger=logger.info) as t:
                translator = manager.get_model(t_p)
                outputs = translator.inference(req.texts)

            outputs = f"{outputs} ({t_p.model_type}: {t.elapsed_time} sec)"

            all_outputs.append(outputs)

        except Exception as e:
            logger.exception(e)

    final_outputs = ""

    logger.info("\n\n")

    logger.info(
        f"EVALUATE TRANSLATORS: {req.from_la} to {req.to_la} with {req.texts}")

    for i, outputs in enumerate(all_outputs):
        logger.info(f"{i} | {outputs}")

        final_outputs = f"{final_outputs}{outputs}\n"

    return final_outputs


@app.post("/translate/")
def translate(req: TranslateRequestParams):
    logger.info(f"{os.getpid()} worker is handling the request")

    if req.from_la == "ko" and req.to_la == "en":
        t_p = TranslateParams(ModelType.OPUS_MT_KO_EN, req.from_la, req.to_la)
    elif (req.from_la == "vi" and req.to_la == "en") or (req.from_la == "en" and req.to_la == "vi"):
        t_p = TranslateParams(ModelType.ENVIT5_TRANSLATION,
                              req.from_la, req.to_la)
    elif req.from_la == "en" and req.to_la == "ja":
        t_p = TranslateParams(ModelType.OPUS_MT_EN_JAP, req.from_la, req.to_la)
        # t_p = TranslateParams(ModelType.MT5_BASE, req.from_la, req.to_la)
        # t_p = TranslateParams(ModelType.MT5_SMALL, req.from_la, req.to_la)
    elif req.to_la == "ja" and req.to_la == "en":
        t_p = TranslateParams(ModelType.OPUS_MT_JA_EN, req.from_la, req.to_la)
    elif req.to_la == "en":
        t_p = TranslateParams(ModelType.OPUS_MT_MUL_EN, req.from_la, req.to_la)
    else:
        t_p = TranslateParams(
            ModelType.MBART_LARGE_50_MANY_TO_MANY, req.from_la, req.to_la)

    logger.debug(f"{t_p=}")
    try:
        with Timer(logger=logger.info) as t:
            translator = manager.get_model(t_p)

            outputs = translator.inference(req.texts)

        outputs_with_time = f"{outputs} (elapsed_time: {t.elapsed_time})"

    except Exception as e:
        logger.exception(e)

    return outputs_with_time


def run_only_once() -> None:
    logger.info("Application is ready now!")


run_only_once()
