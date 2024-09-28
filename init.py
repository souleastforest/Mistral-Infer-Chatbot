import argparse

import torch
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_inference.mamba import Mamba

def load_model(model_path: str, dtype: str):

    if dtype == "float16":
        load_type = torch.float16
    elif dtype == "float32":
        load_type = torch.float32
    elif dtype == "bfloat16":
        load_type = torch.bfloat16
    else:
        raise ValueError(f"Unsupported dtype: {dtype}")

    print("加载分词器...")
    tokenizer = MistralTokenizer.from_file(f"{model_path}/tokenizer.model")
    print("加载模型...")
    model = Mamba.from_folder(model_path, dtype=load_type)
    return model, tokenizer


def parse_args():
    parser = argparse.ArgumentParser(description="Mistral Chatbot API Server")
    parser.add_argument("model_path", type=str, help="Path to the model directory")
    parser.add_argument("--max_tokens", type=int, default=256, help="Maximum number of tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.35, help="Temperature for generation")
    parser.add_argument("--dtype", type=str, default="float16", help="Data type for model (e.g., float32, float16, bf16)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=18000, help="Port to run the server on")
    return parser.parse_args()