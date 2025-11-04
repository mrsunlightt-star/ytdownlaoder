# YouTube Downloader

一个基于 Python 和 PySide6 的跨平台 YouTube 视频下载器，支持最高质量视频下载、多语言字幕（SRT 格式）下载、自定义保存路径、Cookie 导入以及代理配置。

## 功能特性

*   **最高质量视频下载**: 自动选择并下载 YouTube 提供的最高质量视频。
*   **多语言字幕支持**: 可选择下载多种语言的 SRT 格式字幕。
*   **自定义保存路径**: 灵活选择视频和字幕的保存目录。
*   **Cookie 导入**: 支持导入 Netscape 格式的 Cookie 文件，用于绕过地区限制或登录限制。
*   **代理配置**: 支持配置 HTTP/SOCKS 代理，增强下载的稳定性和匿名性。
*   **跨平台兼容**: 针对 macOS 和 Windows 系统进行优化，确保在不同操作系统上都能稳定运行。
*   **内置 FFmpeg**: 优先使用系统 FFmpeg，若未找到则自动使用内置的 `imageio-ffmpeg`，无需手动安装。
*   **用户友好界面**: 简洁直观的中文图形用户界面 (GUI)。

## 安装与运行

### 准备工作

请确保您的系统已安装 Python 3.8 或更高版本。建议使用 [Homebrew](https://brew.sh/) (macOS) 或 [官方安装包](https://www.python.org/downloads/) 安装 Python。

### macOS

#### 方案 A: 一键安装脚本 (推荐)

1.  打开终端，进入项目根目录。
2.  赋予脚本执行权限：
    ```bash
    chmod +x scripts/setup_macos.sh scripts/run_macos.sh
    ```
3.  运行安装脚本：
    ```bash
    ./scripts/setup_macos.sh
    ```
    *   **注意**: 如果系统提示 `xcode-select: note: No developer tools were found, requesting install.`，请按照弹出的窗口提示安装 Command Line Tools。安装完成后，请再次运行 `./scripts/setup_macos.sh`。
    *   脚本会自动检测 Python 环境。如果未找到 Python，它会尝试通过 Homebrew 安装 `python@3.11`。如果 Homebrew 也未安装，脚本会提供安装 Homebrew 的指引。

#### 方案 B: 手动安装 (Homebrew)

1.  安装 [Homebrew](https://brew.sh/) (如果尚未安装)：
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2.  通过 Homebrew 安装 Python 3.11：
    ```bash
    brew install python@3.11
    ```
3.  进入项目根目录，创建并激活虚拟环境：
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

#### 方案 C: 手动安装 (官方 Python 安装包)

1.  从 [Python 官网](https://www.python.org/downloads/) 下载并安装 macOS 版本的 Python 3.11+。
2.  进入项目根目录，创建并激活虚拟环境：
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

### Windows

#### 方案 A: 一键安装脚本 (推荐)

1.  打开 PowerShell (以管理员身份运行，如果遇到执行策略问题)。
2.  进入项目根目录。
3.  运行安装脚本：
    ```powershell
    .\scripts\setup_windows.ps1
    ```
    *   **注意**: 如果遇到执行策略问题，可以尝试运行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`。

#### 方案 B: 手动安装

1.  从 [Python 官网](https://www.python.org/downloads/) 下载并安装 Windows 版本的 Python 3.11+ (确保在安装时勾选 "Add Python to PATH")。
2.  打开命令提示符或 PowerShell，进入项目根目录。
3.  创建并激活虚拟环境：
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate
    ```
4.  安装依赖：
    ```cmd
    pip install -r requirements.txt
    ```

### 运行应用程序

**macOS:**

```bash
./scripts/run_macos.sh
```

**Windows:**

```powershell
.\scripts\run_windows.ps1
```

或者，在激活虚拟环境后，直接运行 `main.py`：

```bash
# macOS/Linux
source .venv/bin/activate
python main.py

# Windows
.venv\Scripts\activate
python main.py
```

## 使用说明

1.  **视频链接**: 在“粘贴视频链接”输入框中输入 YouTube 视频的 URL。
2.  **字幕语言**: 从下拉菜单中选择您希望下载的字幕语言。程序会自动尝试下载 SRT 格式的字幕。
3.  **文件保存到**: 点击“文件保存到”按钮，选择视频和字幕的保存目录。
4.  **导入 Cookie**: 
    *   点击“导入 Cookie”按钮，选择一个 Netscape 格式的 Cookie 文件。这对于下载受限内容或绕过年龄验证非常有用。
    *   **注意**: 目前 macOS 暂不支持直接从 Chrome 浏览器导入 Cookie，需要手动导出 Netscape 格式的 Cookie 文件。
5.  **开始下载**: 点击“开始下载”按钮，程序将开始下载视频和字幕。
6.  **日志区域**: 下载进度和任何错误信息将显示在日志区域中。

## 代理配置 (可选)

如果您需要使用代理，可以在运行脚本前设置 `HTTP_PROXY` 或 `HTTPS_PROXY` 环境变量。例如：

**macOS/Linux:**

```bash
export HTTP_PROXY="http://your_proxy_address:port"
export HTTPS_PROXY="http://your_proxy_address:port"
./scripts/run_macos.sh
```

**Windows (PowerShell):**

```powershell
$env:HTTP_PROXY="http://your_proxy_address:port"
$env:HTTPS_PROXY="http://your_proxy_address:port"
.\scripts\run_windows.ps1
```

## 技术细节

*   **跨平台路径处理**: 使用 `pathlib.Path` 和 `os.path.sep` 确保路径在 macOS 和 Windows 上都能正确处理。
*   **统一换行符**: 文件写入时统一使用 `\n` 作为换行符。
*   **环境变量**: 通过 `os.environ` 统一操作环境变量。
*   **FFmpeg 集成**: `yt-dlp` 会自动检测系统中的 FFmpeg。如果未找到，`imageio-ffmpeg` 会提供一个内置版本。
*   **下载稳定性**: 增加并发下载片段数和重试次数，提高下载成功率。

## 常见问题

*   **`xcode-select` 错误**: 在 macOS 上，首次运行需要 Command Line Tools 的命令时，系统会提示安装。请按照提示安装即可。
*   **下载速度慢或失败**: 尝试配置代理，或检查网络连接。
*   **无法下载受限视频**: 确保已导入正确的 Cookie 文件。

## 许可证

[待定]