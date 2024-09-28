#!/bin/bash

# 查找 fastapi_server.py 的 PID
PID=$(ps aux | grep 'fastapi_server.py' | grep -v grep | awk '{print $2}')

# 如果找到 PID，则尝试关闭程序
if [ -n "$PID" ]; then
    echo "找到 fastapi_server.py 的 PID: $PID"
    kill $PID
    sleep 2  # 等待2秒以确保进程有时间关闭

    # 检查进程是否仍在运行
    if ps -p $PID > /dev/null; then
        echo "进程 $PID 仍在运行，尝试强制关闭..."
        kill -9 $PID
    else
        echo "进程 $PID 已成功关闭。"
    fi
else
    echo "未找到 fastapi_server.py 的运行进程。"
fi
