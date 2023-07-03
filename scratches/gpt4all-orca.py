import asyncio

from gpt4all import GPT4All
from sentence_transformers import SentenceTransformer

model = GPT4All(model_name="orca-mini-3b.ggmlv3.q4_0.bin")


async def run():
    # Simplest invocation
    output = model.generate("The capital of France is ", max_tokens=3)
    print(output)
    embedder = SentenceTransformer("all-MiniLM-L12-v2")
    embed = embedder.encode(output)
    print("type", type(embed))


asyncio.run(run())
