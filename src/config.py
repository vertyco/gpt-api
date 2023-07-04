from decouple import config
from dotenv import load_dotenv

load_dotenv()

# uvicorn
HOST = config("HOST", default="127.0.0.1")
WORKERS = config("WORKERS", default=1, cast=int)
# logging
SENTRY_DSN = config("SENTRY_DSN", default=None)
LOGS_PATH = config("LOGS_PATH", default="")
# GPT4All quantized model
MODEL_NAME = config("MODEL_NAME", default="orca-mini-3b.ggmlv3.q4_0.bin")
BATCH_SIZE = config("BATCH_SIZE", default=2048, cast=int)
# Must be a huggingface model for tokenizing
TOKENIZER = config("TOKENZIER", default="deepset/tinyroberta-squad2")
# Set to
THREADS = config("THREADS", default=None)
MAX_TOKENS = config("MAX_TOKENS", default=750, cast=int)
# embeddings
EMBED_MODEL = config("EMBED_MODEL", default="all-MiniLM-L12-v2")
