$ErrorActionPreference = "Stop" # 遇到错误时停止脚本执行 

$venvDir = ".venv" # 虚拟环境文件夹名称 

# 获取脚本所在目录的父目录，即项目根目录 
$projectRoot = Split-Path -Parent $PSScriptRoot 

# 构建虚拟环境激活脚本的完整路径 
# Join-Path 会自动处理路径分隔符 
$activateScriptPath = Join-Path -Path $projectRoot -ChildPath $venvDir | Join-Path -ChildPath "Scripts" | Join-Path -ChildPath "Activate.ps1" 

# 检查虚拟环境激活脚本是否存在 
if (Test-Path $activateScriptPath) { 
    Write-Host "正在激活虚拟环境..." 
    # 使用点源操作符 '.' 来在当前作用域中运行激活脚本 
    . $activateScriptPath 
} 
else { 
    Write-Error "未在 $activateScriptPath 找到虚拟环境激活脚本，请先运行 setup_windows.ps1" 
    exit 1 
} 

# 构建 main.py 的完整路径并运行主程序 
Write-Host "正在启动 YouTube 下载器..." 
$mainScriptPath = Join-Path -Path $projectRoot -ChildPath "main.py" 
python $mainScriptPath 

# 检查主程序运行结果 
if ($LASTEXITCODE -ne 0) { 
    Write-Error "main.py 运行失败，退出码：$LASTEXITCODE" 
    exit $LASTEXITCODE 
} 

Write-Host "YouTube 下载器运行成功！"