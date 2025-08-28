# src/token_logger.py
import tiktoken
import os


def count_tokens(text: str, model: str = "llama-3.1-8b-instant"):
    try:
        enc = tiktoken.encoding_for_model(model)
    except:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def log_tokens(text: str, model: str = "llama-3.1-8b-instant"):
    tokens = count_tokens(text, model)
    log_dir = "output/logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(f"{log_dir}/token_log.txt", "a") as f:
        f.write(f"{tokens} tokens used\n")
    return tokens
