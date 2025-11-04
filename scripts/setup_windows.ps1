# 设置脚本在遇到错误时终止
$ErrorActionPreference = "Stop"

Write-Host "🚀 正在为 Windows 设置 YouTube Downloader 环境..."

# --- 1. 检查并安装 Python (如果未安装) ---
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "🐍 Python 未安装。请手动安装 Python 3.8+，并确保在安装时勾选 'Add Python to PATH'。"
    Write-Host "您可以访问 https://www.python.org/downloads/windows/ 下载官方安装包。"
    exit 1
}

Write-Host "✅ Python 已安装。"

# --- 2. 创建并激活虚拟环境 ---
$venvDir = ".venv"
if (-not (Test-Path $venvDir)) {
    Write-Host "Creating virtual environment at $venvDir..."
    python -m venv $venvDir
} else {
    Write-Host "Virtual environment already exists at $venvDir. Skipping creation."
}

Write-Host "Activating virtual environment..."
# Windows 激活脚本路径
.$venvDir\Scripts\Activate.ps1

# --- 3. 升级 pip 并安装依赖 ---
Write-Host "Upgrading pip..."
pip install --upgrade pip

Write-Host "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

Write-Host "🎉 环境设置完成！您现在可以运行 .\scripts\run_windows.ps1 来启动应用程序。"