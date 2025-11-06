import sys
import os
from pathlib import Path
import json
import subprocess
import platform

def get_os_type():
    """
    获取操作系统类型。
    """
    return platform.system()

def get_path_separator():
    """
    获取当前操作系统的路径分隔符。
    """
    return os.path.sep

def sanitize_path(input_path: str) -> Path:
    """
    统一处理用户输入的路径，将反斜杠替换为正斜杠，并返回 Path 对象。
    """
    return Path(input_path.replace("\\", "/"))

def get_ffmpeg_path():
    """
    尝试获取 FFmpeg 的路径。
    优先使用系统中的 FFmpeg，如果找不到则使用 imageio-ffmpeg 提供的。
    """
    # 检查系统 PATH 中是否存在 ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True)
        return 'ffmpeg'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 尝试使用 imageio-ffmpeg 提供的 ffmpeg
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path
    except ImportError:
        pass

    return None

def load_cookies_from_file(file_path: Path) -> list:
    """
    从 Netscape 格式的 Cookie 文件中加载 Cookie。
    """
    cookies = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t')
                if len(parts) == 7:
                    domain, flag, path, secure, expiration, name, value = parts
                    cookies.append({
                        'domain': domain,
                        'flag': flag,
                        'path': path,
                        'secure': secure == 'TRUE',
                        'expiration': int(expiration),
                        'name': name,
                        'value': value
                    })
    except Exception as e:
        print(f"加载 Cookie 文件失败: {e}")
    return cookies

def get_chrome_cookies_macos(profile_path: Path) -> list:
    """
    从 macOS Chrome 浏览器中获取 Cookie。
    此功能需要安装 'browser_cookie3' 库，但为了避免增加不必要的依赖，
    这里只提供一个占位符，实际实现可能需要更复杂的逻辑或外部库。
    """
    print("macOS Chrome Cookie 导入功能待实现，请考虑手动导入 Netscape 格式 Cookie 文件。")
    return []

def get_default_download_dir() -> Path:
    """
    获取默认的下载目录。
    """
    home = Path.home()
    if get_os_type() == "Windows":
        return home / "Downloads"
    else:
        return home / "Downloads" # macOS 和 Linux 默认下载目录

def set_environment_variable(key: str, value: str):
    """
    设置环境变量。
    """
    os.environ[key] = value

def get_environment_variable(key: str) -> str:
    """
    获取环境变量。
    """
    return os.environ.get(key, "")

def get_system_encoding() -> str:
    """
    获取系统默认编码。
    """
    return sys.getdefaultencoding()

def get_newline_character() -> str:
    """
    获取系统默认换行符。
    """
    return os.linesep

def write_text_file(file_path: Path, content: str):
    """
    以 UTF-8 编码写入文本文件，并统一使用 \n 作为换行符。
    """
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def read_text_file(file_path: Path) -> str:
    """
    以 UTF-8 编码读取文本文件。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def update_yt_dlp() -> str:
    """
    检查并更新 yt-dlp。
    返回一个表示操作结果的字符串（中文）。
    """
    try:
        # 使用 -U 选项来更新 yt-dlp
        result = subprocess.run(
            [sys.executable, '-m', 'yt_dlp', '-U'],
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        output = result.stdout.strip()
        if "is up to date" in output:
            return "yt-dlp 已是最新版本。"
        elif "Updating to" in output:
            return f"yt-dlp 已成功更新到最新版本。"
        else:
            return "yt-dlp 更新检查完成，未识别到明确状态。"
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        return f"更新 yt-dlp 失败: {error_message}"
    except FileNotFoundError:
        return "未找到 yt-dlp，请确保它已安装在当前 Python 环境中。"
    except Exception as e:
        return f"检查 yt-dlp 更新时发生未知错误: {e}"