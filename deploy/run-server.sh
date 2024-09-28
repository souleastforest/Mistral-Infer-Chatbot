#!/bin/bash

deploydir=$(cd `dirname $0`; pwd)
basedir=$(dirname "$deploydir")
echo "BASEDIR: $basedir"

cd $basedir

if [ ! -d "$basedir/venv" ]; then
    echo "Virtualenv not found"
    exit 1
fi

source $basedir/venv/bin/activate

# 读取 .env 文件
if [ -f "$basedir/.env" ]; then
    export $(grep -v '^#' "$basedir/.env" | xargs)
fi

# 使用环境变量，如果没有设置则使用默认值
MODEL_PATH=${MODEL_PATH:-"/mnt/hdd/llm-proj/model/mistralai/Mamba-Codestral-7B-v0.1"}
MAX_TOKENS=${MAX_TOKENS:-4096}
TEMPERATURE=${TEMPERATURE:-0.35}
DTYPE=${DTYPE:-"float16"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-18000}

# 解析命令行参数（优先级高于环境变量）
while [[ $# -gt 0 ]]; do
    case $1 in
        --model_path)
            MODEL_PATH="$2"
            shift 2
            ;;
        --max_tokens)
            MAX_TOKENS="$2"
            shift 2
            ;;
        --temperature)
            TEMPERATURE="$2"
            shift 2
            ;;
        --dtype)
            DTYPE="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 启动 FastAPI 服务器
nohup python $basedir/fastapi_server.py "$MODEL_PATH" \
    --max_tokens $MAX_TOKENS \
    --temperature $TEMPERATURE \
    --dtype $DTYPE \
    --host $HOST \
    --port $PORT \
    > $basedir/run/logs/fastapi_server.log 2>&1 &

echo "FastAPI 服务器已启动，日志输出到 $basedir/run/logs/fastapi_server.log"