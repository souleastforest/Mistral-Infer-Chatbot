 # Codestral Mamba Server

Mistral AI model server based on Mamba architecture

## System Requirements

- Linux operating system
- Python 3.10+

## Getting Started

1. First, download the model supported by the mistral-inference framework from:
   https://github.com/mistralai/mistral-inference

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file and set the environment variables:

```
MODEL_PATH=/path/to/your/model
MAX_TOKENS=4096
TEMPERATURE=0.35
DTYPE=float16
HOST=0.0.0.0
PORT=18090
```

> The choice of DTYPE depends on your GPU model. For Turing architecture GPUs, use float16; for Ampere architecture GPUs, use bfloat16.
> For example, use float16 for Turing architecture RTX 2080ti 22G, and bfloat16 for Ampere architecture RTX 3090 24G.

## Usage

Make sure to modify the paths in the scripts according to your environment.

### Command-line Chat:

```bash
bash interact-chat.sh <model_path> <max_tokens>
```

### Start the Server:

This script will read the environment variables from the .env file and start the server.

```bash
bash deploy/run-server.sh
```

Or modify the script according to your needs.

### Request 

#### Get Models

```bash
curl -X GET "http://localhost:18090/v1/models"
```

Response example:

```json
{
    "object": "list",
    "data": [
        {
            "id": "Mamba-Codestral-7B-v0.1",
            "object": "model",
            "owned_by": "mistralai",
            "permission": []
        }
    ]
}
```

#### Text Completion

```bash
curl -X POST "http://localhost:18090/v1/engines/completions" -H "Content-Type: application/json" -d '{
  "model": "mistral",
  "prompt": "How expensive would it be to ask a window cleaner to clean all windows in Paris. Make a reasonable guess in US Dollar.",
  "max_tokens": 256,
  "temperature": 0.35
}'
```

Response example:

```json
{
    "id": "cmpl-36d9ad2c-7d02-11ef-a77d-aa1c040f3499",
    "object": "text_completion",
    "created": 1727463393,
    "model": "mistral",
    "choices": [
        {
            "text": "The cost of hiring a window cleaner in Paris, France can vary greatly depending on several factors such as the size of the building, the number of windows, and the level of detail required. However, as a rough estimate, you might expect to pay around $100 to $200 per window for a basic cleaning. If you want a more detailed cleaning, you might pay up to $300 per window. Keep in mind that these are just rough estimates and the actual cost may be higher or lower depending on the specific circumstances.",
            "index": 0,
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 35,
        "completion_tokens": 113,
        "total_tokens": 148
    }
}
```

#### Chat Completion

```bash
curl -X POST "http://localhost:18090/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
  "model": "mistral",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is its population?"}
  ],
  "max_tokens": 256,
  "temperature": 0.35
}'
```

Response example:

```json
{
    "id": "chatcmpl-26da2cb0-7db8-11ef-bcc5-aa1c040f3499",
    "object": "chat.completion",
    "created": 1727541535,
    "model": "mistral",
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "The population of Paris is approximately 2.14 million people."
            },
            "index": 0,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 43,
        "completion_tokens": 15,
        "total_tokens": 58
    }
}
```

Enjoy using it!