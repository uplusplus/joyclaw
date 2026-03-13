#!/bin/bash
# JoyClaw 快速启动脚本 (Linux/Mac)
# 使用方式：chmod +x start_demo.sh && ./start_demo.sh

echo "============================================================"
echo "  JoyClaw AI Agent 快速启动"
echo "============================================================"
echo

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 python3，请确保已安装 Python 3.8+"
    exit 1
fi

echo "[1] 简单工具演示（无需 API Key）"
echo "[2] 完整 AI Agent 演示"
echo "[3] 本地功能测试"
echo
read -p "请选择 (1-3): " choice

case $choice in
    1)
        echo
        echo "运行简单工具演示..."
        python3 examples/simple_demo.py
        ;;
    2)
        echo
        echo "运行完整 AI Agent 演示..."
        python3 examples/demo.py 5
        ;;
    3)
        echo
        echo "运行本地功能测试..."
        python3 test_local_features.py
        ;;
    *)
        echo "[错误] 无效选项"
        exit 1
        ;;
esac

echo
echo "============================================================"
echo "演示完成！"
echo "============================================================"
