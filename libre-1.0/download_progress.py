import os
import sys
import time
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar

class DownloadProgress(QWidget):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Downloading...")
        layout = QVBoxLayout()

        self.label = QLabel(f"Downloading: {self.file_name}")
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.show()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def open_file(self):
        try:
            if os.path.exists(self.file_path):
                subprocess.Popen(f'explorer "{self.file_path}"')
            else:
                QMessageBox.warning(self, "Error", "File does not exist.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloadProgress("example_file.txt")
    for i in range(101):
        time.sleep(0.1)  # Simulate download time
        window.update_progress(i)
    sys.exit(app.exec())
