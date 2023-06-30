from decouple import config
from dotenv import load_dotenv

load_dotenv()

HOST = config("HOST", default="127.0.0.1")
WORKERS = config("WORKERS", default=1, cast=int)

SENTRY_DSN = config("SENTRY_DSN", default=None)
LOGS_PATH = config("LOGS_PATH", default="")

MODEL_NAME = config("MODEL_NAME", default="orca-mini-3b.ggmlv3.q4_0.bin")
MODEL_PATH = config("MODEL_PATH", default=None)
THREADS = config("THREADS", default=None)
EMBED_MODEL = config("EMBED_MODEL", default="all-MiniLM-L12-v2")
LOW_MEMORY = config("LOW_MEMORY", default=False, cast=bool)
