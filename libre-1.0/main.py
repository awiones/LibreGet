import sys
import asyncio
import qasync
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QTabWidget, 
    QFileDialog, QComboBox, QFrame, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QSize, pyqtSlot
from performance import DownloadManager, DownloadStatus, DownloadProgress
import os
from download_progress import DownloadProgress

class DownloadManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Download Manager")
        self.setMinimumSize(800, 400)
        
        # Initialize download manager
        self.download_manager = None
        self.download_items = {}
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Setup UI
        self.create_add_download_section(layout)
        self.create_category_tabs(layout)
        # Removed download queue creation
        # Removed status panel creation
        
        # Apply styling
        self.apply_style()

    def create_add_download_section(self, parent_layout):
        download_frame = QFrame()
        download_frame.setObjectName("addDownloadFrame")
        download_layout = QVBoxLayout(download_frame)
        
        # URL input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter download URL...")
        url_layout.addWidget(QLabel("URL:"))
        url_layout.addWidget(self.url_input)
        
        # Save location
        location_layout = QHBoxLayout()
        self.location_input = QLineEdit()
        self.location_input.setText(str(Path.home() / "Downloads"))
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_location)
        
        location_layout.addWidget(QLabel("Save to:"))
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(browse_button)
        
        # Start download button
        self.start_button = QPushButton("Start Download")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.handle_start_download)
        
        download_layout.addLayout(url_layout)
        download_layout.addLayout(location_layout)
        download_layout.addWidget(self.start_button)
        
        parent_layout.addWidget(download_frame)

    def browse_location(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Save Location",
            self.location_input.text()
        )
        if directory:
            self.location_input.setText(directory)

    def handle_start_download(self):
        """Handle the start download button click"""
        url = self.url_input.text().strip()
        save_path = self.location_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
            
        if not save_path:
            QMessageBox.warning(self, "Error", "Please select a save location")
            return
        
        # Create task for download
        asyncio.create_task(self.start_download(url, save_path))

    async def initialize(self):
        """Initialize the download manager"""
        self.download_manager = DownloadManager(max_concurrent_downloads=3)
        await self.download_manager.initialize()
        # Removed callback for update_download_progress

    async def start_download(self, url: str, save_path: str):
        """Start a new download"""
        try:
            if self.download_manager is None:
                await self.initialize()
            
            download_id = await self.download_manager.add_download(url, save_path)
            # Show download progress UI
            download_progress_ui = DownloadProgress(os.path.basename(save_path))
            download_progress_ui.show()
            
            # Update the download progress in real-time
            self.download_manager.add_callback(download_progress_ui.update_progress)
            
            
            # Show finish download UI after completion
            self.url_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start download: {str(e)}")

        # Removed download queue creation

    def create_category_tabs(self, parent_layout):
        self.tabs = QTabWidget()
        self.tabs.addTab(QWidget(), "All")
        self.tabs.addTab(QWidget(), "Videos")
        self.tabs.addTab(QWidget(), "Music")
        self.tabs.addTab(QWidget(), "Documents")
        self.tabs.setObjectName("categoryTabs")
        parent_layout.addWidget(self.tabs)


        # Removed update_download_progress method

        # Removed create_download_item method

    def update_download_item(self, download_id: str, progress: DownloadProgress):
        """Update an existing download item"""
        if download_id not in self.download_items:
            return
            
        item = self.download_items[download_id]
        
        # Update progress bar
        if progress.total_size > 0:
            percentage = (progress.downloaded / progress.total_size) * 100
            item['progress_bar'].setValue(int(percentage))
        
        # Update speed and time
        item['speed_label'].setText(f"Speed: {self.format_speed(progress.speed)}")
        if progress.speed > 0:
            remaining = (progress.total_size - progress.downloaded) / progress.speed
            item['time_label'].setText(f"Time remaining: {self.format_time(remaining)}")
        
        # Update button states
        item['pause_button'].setEnabled(progress.status == DownloadStatus.DOWNLOADING)
        item['resume_button'].setEnabled(progress.status == DownloadStatus.PAUSED)

    async def pause_download(self, download_id: str):
        """Pause a download"""
        if self.download_manager:
            await self.download_manager.pause_download(download_id)

    async def resume_download(self, download_id: str):
        """Resume a paused download"""
        if self.download_manager:
            await self.download_manager.resume_download(download_id)

    async def cancel_download(self, download_id: str):
        """Cancel a download"""
        if self.download_manager:
            await self.download_manager.cancel_download(download_id)
            if download_id in self.download_items:
                item = self.download_items[download_id]
                self.queue_layout.removeWidget(item['frame'])
                item['frame'].deleteLater()
                del self.download_items[download_id]

    def update_status_panel(self):
        """Update status panel with current statistics"""
        if not self.download_manager:
            return
            
        active_count = 0
        completed_count = 0
        total_speed = 0
        
        for download_id, download in self.download_manager.downloads.items():
            progress = download['progress']
            if progress.status == DownloadStatus.DOWNLOADING:
                active_count += 1
                total_speed += progress.speed
            elif progress.status == DownloadStatus.COMPLETED:
                completed_count += 1
        
        self.total_speed_label.setText(f"Total Speed: {self.format_speed(total_speed)}")
        self.active_downloads_label.setText(f"Active: {active_count}")
        self.completed_downloads_label.setText(f"Completed: {completed_count}")

    @staticmethod
    def format_size(size: int) -> str:
        """Format size in bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    @staticmethod
    def format_speed(speed: float) -> str:
        """Format speed in bytes/second to human readable format"""
        return f"{DownloadManagerGUI.format_size(int(speed))}/s"

    @staticmethod
    def format_time(seconds: float) -> str:
        """Format time in seconds to human readable format"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            seconds = int(seconds % 60)
            return f"{minutes}m {seconds}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"

    def apply_style(self):
        """Apply styling to the application"""
        style = """
            QMainWindow {
                background-color: #e0e0e0; /* Light gray background */
            }
            
            #addDownloadFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            
            #startButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                min-height: 35px;
            }
            
            #startButton:hover {
                background-color: #1976D2;
            }
            
            #downloadItem {
                background-color: white;
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
            
            QProgressBar {
                border: none;
                border-radius: 5px;
                text-align: center;
                background-color: #E0E0E0;
                min-height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
            
            #controlButton {
                background-color: #E0E0E0;
                border: none;
                border-radius: 12px;
            }
            
            #controlButton:hover {
                background-color: #BDBDBD;
            }
            
            #statusPanel {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
            
            QLineEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                background-color: white;
            }
            
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """
        self.setStyleSheet(style)

async def main():
    app = QApplication(sys.argv)
    window = DownloadManagerGUI()
    await window.initialize()  # Initialize the download manager
    window.show()
    
    # Create and run event loop
    loop = asyncio.get_event_loop()
    
    def close_future(future, loop):
        loop.call_later(0.1, future.set_result, None)
    
    # Setup cleanup on application exit
    future = asyncio.Future()
    app.lastWindowClosed.connect(lambda: close_future(future, loop))
    
    # Run the event loop
    try:
        await future
    finally:
        if window.download_manager:
            await window.download_manager.cleanup()

if __name__ == '__main__':
    try:
        qasync.run(main())
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)