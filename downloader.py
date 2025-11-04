import yt_dlp
from pathlib import Path
import threading
import queue
import os

from utils import get_ffmpeg_path, sanitize_path

class DownloadLogger:
    """
    自定义 yt-dlp 日志记录器，将日志消息发送到队列。
    """
    def __init__(self, log_queue: queue.Queue):
        self.log_queue = log_queue

    def debug(self, msg):
        # yt-dlp 可能会输出大量调试信息，这里只记录重要的
        if msg.startswith('[debug]'):
            if "'_format_sort_fields':" in msg or \
               "'_type': 'url'" in msg or \
               "'_version':" in msg:
                return
        self.log_queue.put(msg)

    def info(self, msg):
        self.log_queue.put(msg)

    def warning(self, msg):
        self.log_queue.put(f"WARNING: {msg}")

    def error(self, msg):
        self.log_queue.put(f"ERROR: {msg}")

class YtDlpDownloader(threading.Thread):
    """
    使用 yt-dlp 下载视频的线程类。
    """
    def __init__(self, video_url: str, output_path: Path, subtitle_lang: str, cookie_file: Path = None, proxy: str = None, log_queue: queue.Queue = None):
        super().__init__()
        self.video_url = video_url
        self.output_path = output_path
        self.subtitle_lang = subtitle_lang
        self.cookie_file = cookie_file
        self.proxy = proxy
        self.log_queue = log_queue if log_queue else queue.Queue()
        self.is_running = False

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', d.get('percent_resumed_str', None))
            s = d.get('_speed_str', None)
            e = d.get('_eta_str', None)
            if p and s and e:
                self.log_queue.put(f"下载中: {p} 速度: {s} 预计剩余时间: {e}")
            elif p:
                self.log_queue.put(f"下载中: {p}")
        elif d['status'] == 'finished':
            self.log_queue.put(f"下载完成: {d['filename']}")
        elif d['status'] == 'error':
            self.log_queue.put(f"下载错误: {d['error']}")

    def run(self):
        self.is_running = True
        self.log_queue.put(f"开始下载: {self.video_url}")
        ffmpeg_location = get_ffmpeg_path()
        if not ffmpeg_location:
            self.log_queue.put("ERROR: 未找到 FFmpeg。请确保已安装 FFmpeg 或 imageio-ffmpeg 正常工作。")
            self.is_running = False
            return

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # 优先下载最高质量的 mp4 视频和音频，然后合并
            'outtmpl': str(self.output_path / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'writedescription': False,
            'writeinfojson': False,
            'writesubtitles': True, # 写入字幕
            'subtitleslangs': [self.subtitle_lang], # 指定字幕语言
            'subtitlesformat': 'srt', # 字幕格式为 srt
            'embedsubtitles': False, # 不嵌入字幕
            'convertfilenames': True, # 转换文件名以避免非法字符
            'noplaylist': True, # 不下载播放列表，只下载单个视频
            'progress_hooks': [self._progress_hook],
            'logger': DownloadLogger(self.log_queue),
            'concurrent_fragment_downloads': 5, # 增加并发下载片段数
            'retries': 10, # 增加重试次数
            'fragment_retries': 10,
            'extractor_retries': 10,
            'ignoreerrors': False,
            'ffmpeg_location': ffmpeg_location,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        if self.cookie_file and self.cookie_file.is_file():
            ydl_opts['cookiefile'] = str(self.cookie_file)
            self.log_queue.put(f"使用 Cookie 文件: {self.cookie_file}")

        if self.proxy:
            ydl_opts['proxy'] = self.proxy
            self.log_queue.put(f"使用代理: {self.proxy}")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_url])
        except Exception as e:
            self.log_queue.put(f"下载过程中发生错误: {e}")
        finally:
            self.is_running = False
            self.log_queue.put("下载线程结束。")

    def stop(self):
        self.is_running = False
        self.log_queue.put("下载已取消。")