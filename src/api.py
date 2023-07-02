import asyncio
import logging
import os
from pathlib import Path
from typing import List, Optional, Union

import uvicorn
from fastapi import FastAPI
from gpt4all import GPT4All
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, pipeline
from transformers.pipelines.question_answering import QuestionAnsweringPipeline
from transformers.pipelines.text_generation import TextGenerationPipeline

try:
    import src.config as config
    from src.logger import init_logging, init_sentry
    from src.utils import compile_messages, compile_qa_messages, valid_gpt4all_model
except ModuleNotFoundError:
    import config
    from logger import init_logging, init_sentry
    from utils import compile_messages, compile_qa_messages, valid_gpt4all_model


log = logging.getLogger(__name__)
app = FastAPI(title="GPT API")
model_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "models"
model_path.mkdir(exist_ok=True)
gpt4all_models = GPT4All.list_models()


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


class CompletionInput(BaseModel):
    model: str
    prompt: str
    suffix: Optional[str] = None
    max_tokens: Optional[int] = 16
    temperature: Optional[float] = 1
    top_p: Optional[float] = 1
    n: Optional[int] = 1
    stream: bool = False
    logprobs: Optional[int] = None
    echo: bool = False
    stop: Optional[Union[str, list]] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    best_of: int = 1
    logit_bias: Optional[dict] = None
    user: Optional[str] = None


class EmbedInput(BaseModel):
    model: str
    input: str


class Tokenizing(BaseModel):
    text: str = None
    tokens: list = None


@app.post("/v1/completions")
async def completion(payload: CompletionInput) -> dict:
    def _run() -> dict:
        output = ""
        max_tokens = payload.max_tokens or config.MAX_TOKENS
        if isinstance(model, GPT4All):
            log.debug("Using GPT4All")
            prompt = payload.prompt
            log.debug(f"Prompt: {prompt}")
            output = model.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temp=payload.temperature,
                top_p=payload.top_p,
            )
        elif isinstance(model, QuestionAnsweringPipeline):
            log.debug("Using question-answering")
            prompt = payload.prompt
            split = prompt.split("Context")
            if len(split) < 2:
                output = "None"
            else:
                question = split.pop(-1)
                context = "Context".join(split)
                log.debug(f"Question: {question}")
                log.debug(f"Context: {context}")
                if context:
                    response = model(
                        question=question,
                        context=context,
                        max_tokens=max_tokens,
                        max_length=max_tokens,
                        temperature=payload.temperature,
                    )
                    output = response["answer"] if response else ""
                else:
                    output = "No context found!"
        elif isinstance(model, TextGenerationPipeline):
            log.debug("Using text-generation")
            prompt = payload.prompt
            log.debug(f"Prompt: {prompt}")
            output = model(
                prompt,
                max_new_tokens=max_tokens,
                use_cache=True,
                max_tokens=max_tokens,
                max_length=max_tokens,
                temperature=payload.temperature,
            )
        log.debug(f"Output: {output}")
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


@app.post("/v1/chat/completions")
async def chat(payload: ChatInput) -> dict:
    def _run() -> dict:
        output = ""
        max_tokens = payload.max_tokens or config.MAX_TOKENS

        if isinstance(model, GPT4All):
            log.debug("Using GPT4All")
            prompt = compile_messages(payload.messages)
            log.debug(f"Prompt: {prompt}")
            output = model.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temp=payload.temperature,
                top_p=payload.top_p,
            )
        elif isinstance(model, QuestionAnsweringPipeline):
            log.debug("Using question-answering")
            question, context = compile_qa_messages(payload.messages)
            log.debug(f"Question: {question}")
            log.debug(f"Context: {context}")
            if context:
                response = model(
                    question=question,
                    context=context,
                    max_tokens=max_tokens,
                    max_length=max_tokens,
                    temperature=payload.temperature,
                )
                output = response["answer"] if response else ""
            else:
                output = "No context found!"
        elif isinstance(model, TextGenerationPipeline):
            log.debug("Using text-generation")
            prompt = compile_messages(payload.messages)
            log.debug(f"Prompt: {prompt}")
            output = model(
                prompt,
                max_new_tokens=max_tokens,
                use_cache=True,
                max_tokens=max_tokens,
                max_length=max_tokens,
                temperature=payload.temperature,
            )
        log.debug(f"Output: {output}")
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
    log.debug(f"Incoming text: {payload.input}")
    embedding = await asyncio.to_thread(embedder.encode, payload.input)
    response = {
        "object": "list",
        "data": [{"object": "embedding", "embedding": embedding.tolist(), "index": 0}],
        "model": config.EMBED_MODEL,
        "usage": {"prompt_tokens": 0, "total_tokens": 0},
    }
    return response


@app.post("/v1/tokenize")
async def get_tokens(payload: Tokenizing) -> dict:
    tokens = await asyncio.to_thread(tokenizer.encode, payload.text)
    log.info(f"Tokens: {len(tokens)}")
    return {"tokens": tokens}


@app.post("/v1/untokenize")
async def get_text(payload: Tokenizing) -> dict:
    text = await asyncio.to_thread(tokenizer.convert_tokens_to_string, payload.tokens)
    log.info(f"Text: {text}")
    return {"text": text}


@app.get("/v1/model")
async def get_model() -> dict:
    return {"model": config.MODEL_NAME, "embed_model": config.EMBED_MODEL}


@app.on_event("startup")
async def startup_event():
    def _run():
        global model
        global embedder
        global tokenizer
        threads = int(config.THREADS) if config.THREADS else None
        if valid_gpt4all_model(config.MODEL_NAME, gpt4all_models):
            log.info(f"Spinning up gpt4all model {config.MODEL_NAME} with {threads} threads")
            model = GPT4All(
                model_name=config.MODEL_NAME,
                model_path=model_path.__str__(),
                n_threads=threads,
            )
            tokenizer = AutoTokenizer.from_pretrained(config.TOKENIZER)
        else:
            model = pipeline(
                task="question-answering",
                model=config.MODEL_NAME,
                tokenizer=config.MODEL_NAME,
                low_cpu_mem_usage=config.LOW_MEMORY,
                use_fast=True,
            )
            log.info(f"Model TYPE: {type(model)}")
            tokenizer = model.tokenizer

        embedder = SentenceTransformer(config.EMBED_MODEL)

    init_logging()
    init_sentry(config.SENTRY_DSN)
    log.info(f"Downloading/fetching model: {config.MODEL_NAME}")
    await asyncio.to_thread(_run)
    log.info("Startup complete!")


if __name__ == "__main__":
    uvicorn.run(app=app, host=config.HOST if config.HOST.strip() else "localhost")
