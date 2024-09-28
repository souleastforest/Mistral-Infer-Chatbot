import sys
import os

import asyncio
import uuid
import time
import argparse

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import logging


# 设置工作目录
WORK_DIR = "/mnt/hdd/llm-proj/codestral_mamba"
os.chdir(WORK_DIR)

# 将根目录添加到 Python 的模块搜索路径中
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)


from codestral_mamba.util.setup_log import setup_log
from codestral_mamba.init import parse_args
from mistral_inference.generate import generate_mamba
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

from codestral_mamba.util.lifespan import lifespan

# setup_log()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.35
    dtype: str = "float16"

class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[dict]
    usage: dict

args = parse_args()
logger = logging.getLogger(__name__)

def chat_with_model(model, tokenizer, prompt, **kwargs):
    logger.info(f"Received prompt: {prompt}")
    completion_request = ChatCompletionRequest(messages=[UserMessage(content=prompt)])
    tokens = tokenizer.encode_chat_completion(completion_request).tokens
    logger.info(f"Encoded tokens len: {len(tokens)}")
    out_tokens, _ = generate_mamba([tokens], model, max_tokens=kwargs.get("max_tokens", 256), temperature=kwargs.get("temperature", 0.35), eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id)
    result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
    logger.info(f"Generated tokens len: {len(out_tokens)}")
    logger.info(f"Decoded result: {result}")
    # 计算 token 使用情况
    prompt_tokens = len(tokens)
    completion_tokens = len(out_tokens[0])
    total_tokens = prompt_tokens + completion_tokens

    usage = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens
    }

    return result, usage

app = FastAPI(lifespan=lifespan)

# 创建一个队列来管理请求
request_queue = asyncio.Queue(maxsize=10)

@app.post("/v1/engines/completions", response_model=ChatResponse)
async def create_completion(request: ChatRequest):
    logger.info(f"Received request: {request}")
    if request_queue.full():
        logger.warning("Request queue is full")
        raise HTTPException(status_code=429, detail="Too many requests, please try again later.")
    
    response_future = asyncio.Future()
    await request_queue.put((request, response_future))
    asyncio.create_task(process_queue())
    response_body = await response_future
    response_text, usage = response_body
    response = ChatResponse(
        id=f"cmpl-{uuid.uuid1()}",
        object="text_completion",
        created=int(time.time()),
        model=request.model,
        choices=[{"text": response_text, "index": 0, "logprobs": None, "finish_reason": "stop"}],
        usage=usage
    )
    logger.info(f"Generated response: {response}")
    return response

async def process_queue():
    while not request_queue.empty():
        logger.info("debugging here")
        request, response_future = await request_queue.get()
        logger.info(f"Processing request: {request}")
        try:
            response_text, usage = chat_with_model(app.state.model, app.state.tokenizer, request.prompt, max_tokens=request.max_tokens, temperature=request.temperature, dtype=request.dtype)
            response_future.set_result((response_text, usage))
            logger.info(f"Response text: {response_text}, Usage: {usage}")
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            response_future.set_exception(e)
        finally:
            request_queue.task_done()
            logger.info("Request processed and marked as done")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server")
    uvicorn.run("fastapi_server:app", host=args.host, port=args.port)