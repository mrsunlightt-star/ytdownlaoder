# YouTube Downloader 项目开发记录

## 项目概述
本项目旨在开发一个跨平台的桌面应用程序，用于下载 YouTube 视频和字幕。应用程序将提供一个图形用户界面（GUI），允许用户输入视频链接、选择字幕语言、指定保存路径，并支持通过导入浏览器 Cookie 或手动导入 Cookie 文件来处理受限内容。

## 技术栈
- **编程语言**: Python
- **GUI 框架**: PySide6
- **下载核心**: yt-dlp
- **FFmpeg**: imageio-ffmpeg (内置，作为系统 FFmpeg 的备用)

## 核心功能
1.  **视频下载**: 下载最高质量的 YouTube 视频。
2.  **字幕下载**: 可选下载多语言 SRT 格式字幕。
3.  **自定义保存路径**: 用户可选择视频和字幕的保存目录。
4.  **Cookie 支持**:
    *   macOS: 支持复用 Chrome 浏览器登录状态（Cookie）。
    *   Windows: 支持手动导入 Netscape 格式的 Cookie 文件。
    *   跨平台: 支持手动导入 Netscape 格式的 Cookie 文件。
5.  **代理支持**: 支持配置 HTTP/SOCKS 代理。
6.  **日志区域**: 显示下载进度和状态信息。
7.  **跨平台兼容性**: 代码设计考虑 macOS 和 Windows 系统的差异，例如路径分隔符、换行符、文件权限、文本编码等。

## 界面设计
参照用户提供的 UI 截图，界面将包含以下元素：
-   “导入 Cookie”按钮及对应的 Cookie 文件目录显示框。
-   “粘贴视频链接”输入框。
-   “文件保存到”按钮及对应的文件保存目录显示框。
-   “字幕语言”下拉选择框。
-   “开始下载”按钮。
-   “日志区域”文本框，用于显示下载过程中的信息。

## 开发过程记录

### 2024年7月29日 - 项目初始化与文件重建
-   用户要求重新开始项目，删除所有旧文件。
-   重新创建 `project.md` 文件，记录项目开发过程。

### 2024年7月29日 - macOS 应用程序打包与分发

**目标**：将 Python GUI 应用程序打包成独立的 macOS `.app` 文件，方便用户直接运行。

**步骤**：

1.  **安装 PyInstaller**：
    在虚拟环境中安装 PyInstaller：
    ```bash
    ./.venv/bin/pip install pyinstaller
    ```

2.  **打包应用程序**：
    使用以下命令打包应用程序：
    ```bash
    ./.venv/bin/pyinstaller --noconfirm --onedir --windowed --name "YouTube Downloader" main.py
    ```
    *   `--noconfirm`：自动确认所有提示。
    *   `--onedir`：将所有文件打包到一个文件夹中，生成 `.app` 应用程序包。
    *   `--windowed`：打包为 GUI 应用程序，运行时不显示终端窗口。
    *   `--name "YouTube Downloader"`：设置应用程序名称。
    *   `main.py`：应用程序的入口文件。

3.  **结果**：
    打包完成后，会在项目根目录下生成一个 `dist` 文件夹。其中包含 `YouTube Downloader.app`，这是最终分发给 macOS 用户的应用程序包。

4.  **分发**：
    将 `dist/YouTube Downloader.app` 文件提供给 macOS 用户。用户可以直接双击运行，或将其拖放到“应用程序”文件夹。

**遇到的问题与解决方案**：

*   **PyInstaller 打包后的文件结构**：`dist` 文件夹中包含一个 `YouTube Downloader` 文件夹和一个 `YouTube Downloader.app`。最终分发给用户的是 `YouTube Downloader.app`。

---

## 编码问题解决记录（Windows 系统）
- 问题现象：记事本提示 run_windows.ps1 含 Unicode 字符，保存为 ANSI 会丢失，导致 PowerShell 报 MissingEndCurlyBrace 解析错误
- 解决方法：将 run_windows.ps1 文件编码改为 UTF-8（优先选择「UTF-8 无 BOM」）
- 验证结果：运行简化 if/else 脚本成功输出 "Hello from if block"，确认编码问题已修复
- 后续计划：替换为完整修正版 run_windows.ps1 脚本，验证应用启动正常后，推进 PyInstaller 打包任务

## run_windows.ps1 脚本 ParserError 诊断与解决（Windows 系统）
- 问题现象：运行 run_windows.ps1 脚本时，PowerShell 报错 `表达式或语句中包含意外的标记“}”`，指向 `if` 语句的结束大括号 `}`。
- 诊断：
  1. 确认文件编码已修正为 UTF-8。
  2. 简化 `if/else` 脚本可正常运行，排除基本语法问题。
  3. 怀疑是脚本中路径处理方式或复制粘贴引入的隐形字符导致解析错误。
- 解决方法：
  1. 采用 PowerShell 健壮的 `Join-Path` 命令构建路径，确保跨平台兼容性和路径分隔符的正确性。
  2. 使用点源操作符 `.` 激活虚拟环境脚本，确保在当前作用域运行。
- 后续计划：替换为使用 `Join-Path` 的修正版 `run_windows.ps1` 脚本，并再次运行验证。

## run_windows.ps1 脚本 ParserError 持续问题与手动运行方案（Windows 系统）
- 问题现象：即使在确认文件编码为 UTF-8 并手动输入简化脚本后，`run_windows.ps1` 脚本仍然报告 `表达式或语句中包含意外的标记“}”` 的 `ParserError`。
- 诊断：
  1. 脚本内容从语法上看是正确的，但 PowerShell 报告的错误行号与实际脚本内容不符。
  2. 强烈怀疑是文本编辑器在保存时引入了肉眼不可见的特殊字符，或文件编码问题未彻底解决。
- 解决方案：
  1. 暂时放弃通过 `run_windows.ps1` 脚本启动应用。
  2. 直接在 PowerShell 终端中手动执行命令来激活虚拟环境并运行 `main.py`，以绕过脚本文件本身的潜在问题。
- 后续计划：如果手动运行成功，将继续进行 PyInstaller 打包工作。

## 2025年1月更新：Windows环境重新配置

### 环境重建
- **时间**：2025年1月
- **操作**：重新创建虚拟环境
- **结果**：成功安装所有依赖包（PySide6 6.10.0, yt-dlp 2025.10.22, imageio-ffmpeg 0.6.0等）
- **状态**：应用程序已在 Windows 环境中成功运行，准备进行 PyInstaller 打包。

### PyInstaller 打包 (Windows)
- **目标**：将 Python 应用程序打包成独立的 Windows 可执行文件。
- **步骤**：
    1. **确认 PyInstaller 已安装**：
        - 在激活的虚拟环境中运行 `pip show pyinstaller` 确认。
        - 如果未安装，运行 `pip install pyinstaller`。
    2. **执行打包命令**：
        - 在项目根目录（虚拟环境已激活）下运行以下命令：
        ```powershell
        pyinstaller --onefile --windowed --name="YouTube Downloader" main.py
        ```
        - 如果有 `.ico` 格式的图标文件（例如 `icon.ico` 在项目根目录），可以使用：
        ```powershell
        pyinstaller --onefile --windowed --icon="icon.ico" --name="YouTube Downloader" main.py
        ```
    3. **检查结果**：
        - 打包完成后，在 `dist` 文件夹中查找 `YouTube Downloader.exe`。
- **后续计划**：测试打包后的可执行文件，并进行分发。