#!/bin/bash

# 设置脚本在遇到错误时终止
set -e

echo "🚀 正在启动 YouTube Downloader (macOS)..."

# --- 1. 激活虚拟环境 ---
VENV_DIR=".venv"
if [ -d "${VENV_DIR}" ]; then
    echo "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate"
else
    echo "❌ 虚拟环境未找到。请先运行 ./scripts/setup_macos.sh 进行设置。"
    exit 1
fi

# --- 2. 运行主程序 ---
echo "Running main application..."
python main.py

echo "🎉 应用程序已退出。"