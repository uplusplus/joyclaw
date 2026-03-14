#!/bin/bash
# JoyClaw Web 启动脚本 (Linux/Mac)

echo "============================================================"
echo "  JoyClaw Web 服务启动"
echo "============================================================"
echo

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 python3"
    exit 1
fi

echo "启动 Web 服务..."
echo "访问地址: http://localhost:5000"
echo
echo "按 Ctrl+C 停止服务"
echo "============================================================"
echo

cd web
python3 app.py
