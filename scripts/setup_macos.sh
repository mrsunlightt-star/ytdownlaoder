#!/bin/bash

# 设置脚本在遇到错误时终止
set -e

echo "🚀 正在为 macOS 设置 YouTube Downloader 环境..."

# --- 1. 检查并安装 Homebrew (如果未安装) ---
if ! command -v brew &> /dev/null;
then
    echo "🍺 Homebrew 未安装，正在安装 Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # 确保 Homebrew 在 PATH 中
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "✅ Homebrew 已安装。"
fi

# --- 2. 检查并安装 Python 3.11 (如果未安装) ---
PYTHON_VERSION="3.11"
PYTHON_BIN="python${PYTHON_VERSION}"

if ! command -v ${PYTHON_BIN} &> /dev/null;
then
    echo "🐍 Python ${PYTHON_VERSION} 未安装，正在通过 Homebrew 安装..."
    brew install python@${PYTHON_VERSION}
    # 确保新安装的 Python 在 PATH 中
    eval "$(/opt/homebrew/bin/brew shellenv)"
    if ! command -v ${PYTHON_BIN} &> /dev/null;
    then
        echo "❌ 无法通过 Homebrew 安装 Python ${PYTHON_VERSION}。请尝试手动安装 Python ${PYTHON_VERSION}，然后重新运行此脚本。"
        echo "您可以访问 https://www.python.org/downloads/macos/ 下载官方安装包。"
        exit 1
    fi
else
    echo "✅ Python ${PYTHON_VERSION} 已安装。"
fi

# 确保使用正确的 python3 命令，优先使用 Homebrew 安装的
PYTHON_EXECUTABLE=$(brew --prefix python@${PYTHON_VERSION})/bin/${PYTHON_BIN}
if [ ! -f "${PYTHON_EXECUTABLE}" ]; then
    PYTHON_EXECUTABLE=$(which python3)
fi

echo "使用 Python 可执行文件: ${PYTHON_EXECUTABLE}"

# --- 3. 创建并激活虚拟环境 ---
VENV_DIR=".venv"
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating virtual environment at ${VENV_DIR}..."
    "${PYTHON_EXECUTABLE}" -m venv "${VENV_DIR}"
else
    echo "Virtual environment already exists at ${VENV_DIR}. Skipping creation."
fi

echo "Activating virtual environment..."
source "${VENV_DIR}/bin/activate"

# --- 4. 升级 pip 并安装依赖 ---
echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "🎉 环境设置完成！您现在可以运行 ./scripts/run_macos.sh 来启动应用程序。"