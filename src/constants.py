# Size and RAM are in GB
LOCAL_MODELS = {
    "deepset/tinyroberta-squad2": {
        "name": "Tiny Roberta",
        "size": 0.326,
        "ram": 0.8,
    },
    "deepset/roberta-base-squad2": {
        "name": "Roberta Base",
        "size": 0.496,
        "ram": 0.73,
    },
    "deepset/roberta-large-squad2": {
        "name": "Roberta Large",
        "size": 1.42,
        "ram": 1.64,
    },
}
LOCAL_GPT_MODELS = {
    "nous-hermes-13b.ggmlv3.q4_0.bin": {
        "name": "Hermes",
        "size": 6.82,
        "ram": 16,
        "params": "13 billion",
    },
    "ggml-model-gpt4all-falcon-q4_0.bin": {
        "name": "GPT4ALL Falcon",
        "size": 4.06,
        "ram": 8,
        "params": "7 billion",
    },
    "ggml-gpt4all-j-v1.3-groovy.bin": {
        "name": "Groovy",
        "size": 3.53,
        "ram": 8,
        "params": "7 billion",
    },
    "GPT4All-13B-snoozy.ggmlv3.q4_0.bin": {
        "name": "Snoozy",
        "size": 7.58,
        "ram": 16,
        "params": "13 billion",
    },
    "ggml-mpt-7b-chat.bin": {
        "name": "MPT Chat",
        "size": 4.52,
        "ram": 8,
        "params": "7 billion",
    },
    "orca-mini-7b.ggmlv3.q4_0.bin": {
        "name": "Orca",
        "size": 3.53,
        "ram": 8,
        "params": "7 billion",
    },
    "orca-mini-3b.ggmlv3.q4_0.bin": {
        "name": "Orca (Small)",
        "size": 1.8,
        "ram": 4,
        "params": "3 billion",
    },
    "orca-mini-13b.ggmlv3.q4_0.bin": {
        "name": "Orca (Large)",
        "size": 6.82,
        "ram": 16,
        "params": "13 billion",
    },
    "ggml-vicuna-7b-1.1-q4_2.bin": {
        "name": "Vicuna",
        "size": 3.92,
        "ram": 8,
        "params": "7 billion",
    },
    "ggml-vicuna-13b-1.1-q4_2.bin": {
        "name": "Vicuna (Large)",
        "size": 7.58,
        "ram": 16,
        "params": "13 billion",
    },
    "ggml-wizardLM-7B.q4_2.bin": {
        "name": "Wizard",
        "size": 3.92,
        "ram": 8,
        "params": "7 billion",
    },
    "wizardLM-13B-Uncensored.ggmlv3.q4_0.bin": {
        "name": "Wizard Uncensored",
        "size": 7.58,
        "ram": 16,
        "params": "13 billion",
    },
}
LOCAL_EMBED_MODELS = [
    "all-MiniLM-L6-v2",  # 80MB download, 350MB RAM
    "all-MiniLM-L12-v2",  # 120MB download, 650MB RAM (RECOMMENDED)
    "all-mpnet-base-v2",  # 420MB download, 750MB RAM
]
