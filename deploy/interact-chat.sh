#!/bin/bash

# 检查是否提供了第一个参数（模型路径）
if [ -z "$1" ]; then
  echo "错误: 需要提供模型路径作为第一个参数。"
  echo "用法: $0 <model_path> <max_tokens>"
  exit 1
fi

# 检查是否提供了第二个参数（最大tokens数量）
if [ -z "$2" ]; then
  echo "错误: 需要提供最大tokens数量作为第二个参数。"
  echo "用法: $0 <model_path> <max_tokens>"
  exit 1
fi

# 设置 CUDA 架构列表
export TORCH_CUDA_ARCH_LIST="7.5"

# 运行 Python 脚本
./venv/bin/python ../chat.py "$1" --instruct --max_tokens "$2"