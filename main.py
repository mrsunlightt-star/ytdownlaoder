import sys
import os
from pathlib import Path
import queue
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QComboBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import Signal, QThread

from downloader import YtDlpDownloader
from utils import get_default_download_dir, sanitize_path, load_cookies_from_file, get_chrome_cookies_macos, get_os_type, update_yt_dlp

class LogThread(QThread):
    log_signal = Signal(str)

    def __init__(self, log_queue: queue.Queue):
        super().__init__()
        self.log_queue = log_queue
        self.running = True

    def run(self):
        while self.running:
            try:
                message = self.log_queue.get(timeout=0.1)
                self.log_signal.emit(message)
            except queue.Empty:
                continue

    def stop(self):
        self.running = False
        self.wait()

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.downloader_thread = None
        self.log_queue = queue.Queue()
        self.log_thread = LogThread(self.log_queue)
        self.log_thread.log_signal.connect(self.update_log)
        self.log_thread.start()

        self.init_ui()
        self.load_settings()
        self.check_for_updates()

    def init_ui(self):
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Title
        title_label = QLabel("YouTube Downloader")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Cookie import section
        cookie_layout = QHBoxLayout()
        self.import_cookie_button = QPushButton("导入 Cookie")
        self.import_cookie_button.clicked.connect(self.import_cookie_file)
        cookie_layout.addWidget(self.import_cookie_button)

        self.cookie_path_input = QLineEdit()
        self.cookie_path_input.setPlaceholderText("cookies 文件存在的目录 (可选)")
        self.cookie_path_input.setReadOnly(True)
        cookie_layout.addWidget(self.cookie_path_input)
        main_layout.addLayout(cookie_layout)

        # Video link section
        video_link_layout = QHBoxLayout()
        video_link_label = QLabel("粘贴视频链接")
        video_link_layout.addWidget(video_link_label)
        self.video_link_input = QLineEdit()
        self.video_link_input.setPlaceholderText("在此粘贴 YouTube 视频链接")
        video_link_layout.addWidget(self.video_link_input)
        main_layout.addLayout(video_link_layout)

        # Save directory section
        save_dir_layout = QHBoxLayout()
        self.save_dir_button = QPushButton("文件保存到")
        self.save_dir_button.clicked.connect(self.select_save_directory)
        save_dir_layout.addWidget(self.save_dir_button)

        self.save_dir_input = QLineEdit(str(get_default_download_dir()))
        self.save_dir_input.setPlaceholderText("用户的文件目录")
        self.save_dir_input.setReadOnly(True)
        save_dir_layout.addWidget(self.save_dir_input)
        main_layout.addLayout(save_dir_layout)

        # Subtitle language and download button section
        action_layout = QHBoxLayout()
        subtitle_lang_label = QLabel("字幕语言")
        action_layout.addWidget(subtitle_lang_label)
        self.subtitle_lang_combo = QComboBox()
        self.subtitle_lang_combo.addItems(['zh-Hans', 'en', 'ja', 'ko', 'fr', 'de', 'es', 'it', 'ru', 'ar', 'pt', 'hi', 'th', 'tr', 'vi'])
        self.subtitle_lang_combo.setCurrentText('zh-Hans') # Default to Simplified Chinese
        action_layout.addWidget(self.subtitle_lang_combo)

        self.start_download_button = QPushButton("开始下载")
        self.start_download_button.clicked.connect(self.start_download)
        action_layout.addWidget(self.start_download_button)
        main_layout.addLayout(action_layout)

        # Log area
        log_label = QLabel("日志区域")
        main_layout.addWidget(log_label)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        main_layout.addWidget(self.log_output)

        self.setLayout(main_layout)

    def check_for_updates(self):
        self.log_queue.put("正在检查 yt-dlp 更新...")
        update_thread = threading.Thread(target=self._run_update_check)
        update_thread.daemon = True
        update_thread.start()

    def _run_update_check(self):
        update_message = update_yt_dlp()
        self.log_queue.put(update_message)

    def load_settings(self):
        # Load previously saved settings if any
        # For simplicity, we'll just set default download dir for now
        pass

    def import_cookie_file(self):
        if get_os_type() == "Darwin": # macOS
            # For macOS, try to get Chrome cookies directly
            # This part is complex and usually requires external libraries like browser_cookie3
            # For now, we'll just allow selecting a Netscape format cookie file
            QMessageBox.information(self, "提示", "macOS 暂不支持直接导入 Chrome Cookie。请手动导出 Netscape 格式的 Cookie 文件并选择。")

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择 Cookie 文件", str(Path.home()), "Cookie Files (*.txt);;All Files (*)")
        if file_path:
            self.cookie_path_input.setText(file_path)
            self.log_queue.put(f"已选择 Cookie 文件: {file_path}")

    def select_save_directory(self):
        dir_dialog = QFileDialog()
        dir_path = dir_dialog.getExistingDirectory(self, "选择保存目录", str(get_default_download_dir()))
        if dir_path:
            self.save_dir_input.setText(dir_path)
            self.log_queue.put(f"已选择保存目录: {dir_path}")

    def start_download(self):
        video_url = self.video_link_input.text().strip()
        if not video_url:
            QMessageBox.warning(self, "警告", "请输入视频链接！")
            return

        output_path = sanitize_path(self.save_dir_input.text())
        if not output_path.is_dir():
            try:
                output_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建保存目录: {e}")
                return

        subtitle_lang = self.subtitle_lang_combo.currentText()
        cookie_file = Path(self.cookie_path_input.text()) if self.cookie_path_input.text() else None

        if self.downloader_thread and self.downloader_thread.is_running:
            QMessageBox.information(self, "提示", "下载正在进行中，请等待当前下载完成或重启应用。")
            return

        self.log_output.clear()
        self.log_queue.put("开始初始化下载...")

        self.downloader_thread = YtDlpDownloader(
            video_url=video_url,
            output_path=output_path,
            subtitle_lang=subtitle_lang,
            cookie_file=cookie_file,
            log_queue=self.log_queue
        )
        self.downloader_thread.start()

    def update_log(self, message):
        self.log_output.append(message)

    def closeEvent(self, event):
        if self.log_thread and self.log_thread.running:
            self.log_thread.stop()
        if self.downloader_thread and self.downloader_thread.is_running:
            self.downloader_thread.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec())