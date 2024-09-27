import argparse

import torch
from mistral_inference.mamba import Mamba
from mistral_inference.generate import generate_mamba

from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

def parse_args():
    parser = argparse.ArgumentParser(description="Mistral Chatbot")
    parser.add_argument("model_path", type=str, help="Path to the model directory")
    parser.add_argument("--instruct", action="store_true", help="Use instruct mode")
    parser.add_argument("--max_tokens", type=int, default=256, help="Maximum number of tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.35, help="Temperature for generation")
    parser.add_argument("--dtype", type=str, default="float16", help="Data type for model (e.g., float32, float16, bf16)")
    return parser.parse_args()

def main():
    args = parse_args()

    # 加载模型和分词器
    print("加载分词器...")
    tokenizer = MistralTokenizer.from_file(f"{args.model_path}/tokenizer.model")
    print("加载模型...")
    model = Mamba.from_folder(args.model_path, dtype=torch.float16)

    print("模型和分词器加载完成。")

    def chat_with_model(prompt):
        completion_request = ChatCompletionRequest(messages=[UserMessage(content=prompt)])
        tokens = tokenizer.encode_chat_completion(completion_request).tokens
        out_tokens, _ = generate_mamba([tokens], model, max_tokens=args.max_tokens, temperature=args.temperature, eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id)
        result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
        return result

    print("欢迎使用聊天机器人！输入<quit>退出。")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "<quit>":
            print("退出聊天。")
            break
        print("生成回复中，请稍候...")
        response = chat_with_model(user_input)
        print(f"bot: {response}")

if __name__ == "__main__":
    main()