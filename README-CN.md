# Codestral Mamba Server

基于 Mamba 架构的 Mistral AI 模型服务器

## 环境要求

- Linux 操作系统
- Python 3.10+

## 开始使用

1. 首先，从以下地址下载mistral-inference推理框架支持的模型：
   https://github.com/mistralai/mistral-inference

2. 创建并激活虚拟环境：

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. 创建 `.env` 文件并设置环境变量：

```
MODEL_PATH=/path/to/your/model
MAX_TOKENS=4096
TEMPERATURE=0.35
DTYPE=float16
HOST=0.0.0.0
PORT=18090
```

> DTYPE的选择根据你的显卡模型决定，对于turing架构的显卡，使用float16，对于ampere架构的显卡，使用bfloat16。
> 例如，turing架构的rtx 2080ti 22G 使用float16，ampere架构的rtx 3090 24G 可以使用bfloat16。

## 使用方法

确保根据您的环境修改脚本中的路径。

## 命令行聊天：

```
bash interact-chat.sh <model_path> <max_tokens>
```

## 启动服务器：

这个脚本会读取 .env 文件中的环境变量，并启动服务器。    

```
bash deploy/run-server.sh
```

或者根据你的需要修改脚本。

### 请求示例

```

curl -X POST "http://localhost:18000/v1/engines/completions" -H "Content-Type: application/json" -d '{
  "model": "mistral",
  "prompt": "How expensive would it be to ask a window cleaner to clean all windows in Paris. Make a reasonable guess in US Dollar.",
  "max_tokens": 256,
  "temperature": 0.35
}'

```

响应示例：

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

享受使用吧！
