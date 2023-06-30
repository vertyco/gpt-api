import asyncio
import logging
from typing import List, Optional, Union

from fastapi import FastAPI
from gpt4all import GPT4All
from pydantic import BaseModel

import src.config as config
from src.logger import init_logging, init_sentry

# from sentence_transformers import SentenceTransformer

log = logging.getLogger(__name__)
app = FastAPI(title="GPT API")
model: GPT4All = None
embedder = None


class ChatInput(BaseModel):
    model: str
    messages: List[dict]
    functions: Optional[list] = None
    function_call: Optional[str] = "autto"
    temperature: Optional[float] = 1
    top_p: Optional[float] = 1
    n: Optional[int] = 1
    stream: Optional[bool] = None
    stop: Optional[Union[str, list]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[dict] = None
    user: Optional[str] = None


class EmbedInput(BaseModel):
    model: str
    input: str


@app.post("/v1/chat/completions")
async def chat(payload: ChatInput) -> dict:
    def _run() -> dict:
        return model.chat_completion(
            messages=payload.messages,
            temp=payload.temperature,
            top_p=payload.top_p,
            verbose=False,
            streaming=False,
        )

    if not model:
        return {"status": 500}
    return await asyncio.to_thread(_run)


# @app.post("/v1/embeddings")
# async def embed(payload: EmbedInput) -> dict:
#     embedding = await asyncio.to_thread(embedder.encode, payload.input)
#     response = {
#         "object": "list",
#         "data": [{"object": "embedding", "embedding": embedding, "index": 0}],
#         "model": config.EMBED_MODEL,
#         "usage": {"prompt_tokens": 0, "total_tokens": 0},
#     }
#     return response


@app.on_event("startup")
async def startup_event():
    def _run():
        global model
        model = GPT4All(
            model_name=config.MODEL_NAME,
            model_path=config.MODEL_PATH,
            n_threads=int(config.THREADS) if config.THREADS else None,
        )
        # embedder = SentenceTransformer(config.EMBED_MODEL)

    init_logging()
    init_sentry(config.SENTRY_DSN)
    log.info(f"Downloading/fetching model: {config.MODEL_NAME}")
    await asyncio.to_thread(_run)
