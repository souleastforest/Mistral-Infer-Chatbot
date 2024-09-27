from contextlib import asynccontextmanager
from fastapi import FastAPI

from codestral_mamba.init import load_model, parse_args
from codestral_mamba.util.setup_log import setup_log

args = parse_args()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # init log
    setup_log()

    # 加载模型和分词器
    print("加载分词器和模型...")
    global model, tokenizer
    app.state.model, app.state.tokenizer = load_model(args.model_path, args.dtype)
    print("模型和分词器加载完成。")

    # ⬆︎⬆︎⬆︎⬆︎⬆︎⬆︎⬆︎⬆︎
    # before startup

    yield

    # ⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎⬇︎
    # after shutdown

    # 卸载模型和分词器
    del app.state.model
    del app.state.tokenizer
    print("模型和分词器已卸载。")