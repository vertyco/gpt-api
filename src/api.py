import asyncio
import os
from configparser import ConfigParser
from pathlib import Path
from typing import List, Optional, Union

from fastapi import FastAPI
from gpt4all import GPT4All
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from src.logger import init_logging

app = FastAPI()
init_logging()
root = os.path.dirname(os.path.abspath(__file__))

parser = ConfigParser()
parser.read(Path(root) / "config.ini")
settings = parser["Settings"]
model_name = settings.get("ModelName", fallback="nous-hermes-13b.ggmlv3.q4_0.bin")
model_path = settings.get("ModelPath", fallback=None)
threads = settings.getint("Threads", fallback=None)

embed_model = settings.get("EmbedModel", fallback="all-MiniLM-L12-v2")
low_mem = settings.getboolean("LowMemory", fallback=True)

if not threads:
    threads = None
if not model_path:
    model_path = None

gpt: GPT4All = GPT4All(model_name=model_name.strip(), model_path=model_path, n_threads=threads)
embedder: SentenceTransformer = SentenceTransformer(embed_model)


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
        return gpt.chat_completion(
            messages=payload.messages,
            temp=payload.temperature,
            top_p=payload.top_p,
            verbose=False,
            streaming=False,
        )

    return await asyncio.to_thread(_run)


@app.post("/v1/embeddings")
async def embed(payload: EmbedInput):
    await asyncio.to_thread(embedder.encode, payload.input)


@app.on_event("startup")
async def startup_event():
    init_logging()
