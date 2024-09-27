# Getting Start

env: linux

first, download model from here:
https://github.com/mistralai/mistral-inference

assume model in `models` file

```
python -m venv venv
pip install -r requirements.txt
```

# usage

(ensure modify path in script depends your env)

## command line chat:

```
bash interact-chat.sh <model_path> <max_tokens>
```

## server

```
bash deploy-server.sh
```

if you want run in backend, run with nohup command:

```

bash nohup deploy-server.sh

```

or modify script by yourself.

### request

```

curl -X POST "http://localhost:18000/v1/engines/completions" -H "Content-Type: application/json" -d '{
  "model": "mistral",
  "prompt": "How expensive would it be to ask a window cleaner to clean all windows in Paris. Make a reasonable guess in US Dollar.",
  "max_tokens": 256,
  "temperature": 0.35
}'

```

response example:

```
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

enjoy!