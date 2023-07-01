import asyncio
import logging
import os
from pathlib import Path
from typing import List, Optional, Union

from fastapi import FastAPI
from gpt4all import GPT4All
from pydantic import BaseModel

try:
    import src.config as config
    from src.logger import init_logging, init_sentry
    from src.utils import compile_messages
except ModuleNotFoundError:
    import config
    from logger import init_logging, init_sentry
    from utils import compile_messages

from sentence_transformers import SentenceTransformer

log = logging.getLogger(__name__)
app = FastAPI(title="GPT API")
model_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "models"
model_path.mkdir(exist_ok=True)


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
        prompt = compile_messages(payload.messages)
        log.debug(f"Incoming prompt: {prompt}")
        output = model.generate(
            prompt=prompt,
            max_tokens=payload.max_tokens,
            temp=payload.temperature,
            top_p=payload.top_p,
        )
        response = {
            "object": "list",
            "choices": [{"message": {"content": output}}],
            "model": config.EMBED_MODEL,
            "usage": {"prompt_tokens": 0, "total_tokens": 0},
        }
        return response

    if not model:
        return {"status": 500, "message": "Model not initialized!"}
    return await asyncio.to_thread(_run)


@app.post("/v1/embeddings")
async def embed(payload: EmbedInput) -> dict:
    embedding = await asyncio.to_thread(embedder.encode, payload.input)
    response = {
        "object": "list",
        "data": [{"object": "embedding", "embedding": embedding, "index": 0}],
        "model": config.EMBED_MODEL,
        "usage": {"prompt_tokens": 0, "total_tokens": 0},
    }
    return response


@app.on_event("startup")
async def startup_event():
    def _run():
        global model
        model = GPT4All(
            model_name=config.MODEL_NAME,
            model_path=model_path.__str__(),
            n_threads=int(config.THREADS) if config.THREADS else None,
        )
        global embedder
        embedder = SentenceTransformer(config.EMBED_MODEL)

    init_logging()
    init_sentry(config.SENTRY_DSN)
    log.info(f"Downloading/fetching model: {config.MODEL_NAME}")
    await asyncio.to_thread(_run)
