# 设置脚本在遇到错误时终止
$ErrorActionPreference = "Stop"

Write-Host "🚀 正在启动 YouTube Downloader (Windows)..."

# --- 1. 激活虚拟环境 ---
$venvDir = ".venv"
if (Test-Path $venvDir) {
    Write-Host "Activating virtual environment..."
    # Windows 激活脚本路径
    .$venvDir\Scripts\Activate.ps1
} else {
    Write-Host "❌ 虚拟环境未找到。请先运行 .\scripts\setup_windows.ps1 进行设置。"
    exit 1
}

# --- 2. 运行主程序 ---
Write-Host "Running main application..."
python main.py

Write-Host "🎉 应用程序已退出。"