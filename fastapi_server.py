import os
import sys
import textwrap
import time
import uuid
import asyncio
import logging
from pydantic import BaseModel
from typing import List

from fastapi import FastAPI, HTTPException, BackgroundTasks
from mistral_inference.generate import generate_mamba
from mistral_common.protocol.instruct.messages import UserMessage, ChatMessage, SystemMessage, AssistantMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

import uvicorn

from init import parse_args
from util.lifespan import lifespan
from qa_pairs import QAPairs

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

class CustomChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: int = 256
    temperature: float = 0.35
    dtype: str = "float16"

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[dict]
    usage: dict

qa_pairs = QAPairs()

args = parse_args()

class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    owned_by: str = "mistralai"
    permission: List[dict] = []

class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]

def chat_with_model(model, tokenizer, completion_request, **kwargs):
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
    

    logger.info(f"Received prompt: {request.prompt}")
    completion_request = CustomChatCompletionRequest(
        model=request.model,
        messages=[UserMessage(content=request.prompt)],
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        dtype=request.dtype
    )
    
    response_future = asyncio.Future()
    await request_queue.put((completion_request, response_future))
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

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: CustomChatCompletionRequest):
    logger.info(f"Received chat completion request: {request}")
    if request_queue.full():
        logger.warning("Request queue is full")
        raise HTTPException(status_code=429, detail="Too many requests, please try again later.")
    
    # message_list = get_chat_template(request.messages)
    messages_list = check_messages(request.messages)
    logger.info(f"Message list: {messages_list}")
    completion_request = CustomChatCompletionRequest(
        model=request.model,
        messages=messages_list,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        dtype=request.dtype
    )
    
    response_future = asyncio.Future()
    await request_queue.put((completion_request, response_future))
    asyncio.create_task(process_queue())
    response_body = await response_future
    response_text, usage = response_body
    
    response = ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid1()}",
        object="chat.completion",
        created=int(time.time()),
        model=request.model,
        choices=[{"message": {"role": "assistant", "content": response_text}, "index": 0, "finish_reason": "stop", "logprobs": None}],
        usage=usage
    )
    logger.info(f"Generated chat completion response: {response}")
    return response

@app.get("/v1/models", response_model=ModelsResponse)
async def list_models():
    model_name = os.path.basename(args.model_path)
    model_info = ModelInfo(id=model_name)
    return ModelsResponse(data=[model_info])


def check_messages(messages: List[ChatMessage]) -> List[ChatMessage]:
    if len(messages) == 0:
        raise HTTPException(status_code=400, detail="Messages list is empty")
    if len(messages) == 1:
        if messages[0].role != "system":
            # 设置默认的 system message
            messages.insert(0, SystemMessage(content="You are a helpful assistant."))
    if len(messages) == 2:
        if messages[0].role != "system":
            # 设置默认的 system message
            messages.insert(0, SystemMessage(content="You are a helpful assistant."))
        if messages[1].role != "user":
            raise HTTPException(status_code=400, detail="The second message must be a user message")
    if len(messages) > 2:
        if messages[0].role != "system":
            # 设置默认的 system message
            messages.insert(0, SystemMessage(content="You are a helpful assistant."))
        if messages[1].role != "user":
            raise HTTPException(status_code=400, detail="The second message must be a user message")
        if messages[-1].role != "user":
            raise HTTPException(status_code=400, detail="The last message must be a user message")
    return messages


def get_chat_template(messages: List[ChatMessage]) -> List[ChatMessage]:
    system_message = ""
    conversation_history = []
    user_message = ""

    for msg in messages:
        if msg.role == "system":
            system_message = msg.content
        elif msg.role == "user":
            if conversation_history or user_message:
                conversation_history.append(f"<s>[INST] User: {user_message} [/INST]</s>")
            user_message = msg.content
        elif msg.role == "assistant":
            conversation_history.append(f"<s>[INST] Assistant: {msg.content} [/INST]</s>")

    conversation_str = "\n".join(conversation_history)
    
    template = textwrap.dedent(f"""
        <s>[INST] system: {system_message} \n\n
        {conversation_str}
        User: {user_message} [/INST]</s>
        <s>[INST] Assistant: 
    """)

    template_old = f"""
        System: {system_message} \n\n

        {conversation_str}
        User: {user_message}
        Assistant: 
    """

    return template.strip()

async def process_queue():
    while not request_queue.empty():
        logger.info("debugging here")
        request, response_future = await request_queue.get()
        logger.info(f"Processing request: {request}")
        try:
            chat_request = ChatCompletionRequest(
                messages=request.messages,
            )
            response_text, usage = chat_with_model(app.state.model, app.state.tokenizer, chat_request, max_tokens=request.max_tokens, temperature=request.temperature, dtype=request.dtype)
            response_future.set_result((response_text, usage))
            logger.info(f"Response text: {response_text}, Usage: {usage}")
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            response_future.set_exception(e)
        finally:
            request_queue.task_done()
            logger.info("Request processed and marked as done")

if __name__ == "__main__":
    logger.info(f"Working dir: {os.getcwd()}")
    logger.info(f"Loading model from path: {args.model_path}")
    logger.info("Starting FastAPI server")
    uvicorn.run("fastapi_server:app", host=args.host, port=args.port)