import asyncio
import os
from configparser import ConfigParser
from pathlib import Path
from typing import List, Optional, Union

from fastapi import FastAPI
from gpt4all import GPT4All
from pydantic import BaseModel

app = FastAPI()

root = os.path.dirname(os.path.abspath(__file__))

parser = ConfigParser()
parser.read(Path(root) / "config.ini")
settings = parser["Settings"]
model_name = settings.get("ModelName", fallback="nous-hermes-13b.ggmlv3.q4_0.bin")
model_path = settings.get("ModelPath", fallback=None)
threads = settings.getint("Threads", fallback=None)

if not threads:
    threads = None
if not model_path:
    model_path = None

gpt: GPT4All = GPT4All(model_name=model_name, model_path=model_path, n_threads=threads)


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


def _get_response(payload: ChatInput) -> dict:
    return gpt.chat_completion(
        messages=payload.messages,
        temp=payload.temperature,
        top_p=payload.top_p,
        verbose=False,
        streaming=False,
    )


@app.post("/chat/completions")
async def chat(payload: ChatInput) -> dict:
    return await asyncio.to_thread(_get_response, payload)
