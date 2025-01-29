import asyncio

class DownloadStatus:
    DOWNLOADING = "downloading"
    COMPLETED = "completed"

class DownloadProgress:
    def __init__(self):
        self.downloaded = 0
        self.total_size = 0
        self.status = DownloadStatus.DOWNLOADING

class DownloadManager:
    def initialize(self):
        self.downloads.clear()  # Clear any existing downloads
        self.callbacks.clear()   # Clear any existing callbacks
    def __init__(self, max_concurrent_downloads):
        self.max_concurrent_downloads = max_concurrent_downloads
        self.downloads = {}
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    async def add_download(self, url, save_path):
        download_id = str(len(self.downloads) + 1)
        self.downloads[download_id] = {
            'url': url,
            'save_path': save_path,
            'progress': DownloadProgress()
        }
        await self.start_download(download_id)
        return download_id

    async def start_download(self, download_id):
        # Simulate download process
        total_size = 100  # Simulated total size
        for downloaded in range(total_size + 1):
            await asyncio.sleep(0.1)  # Simulate time taken to download
            self.downloads[download_id]['progress'].downloaded = downloaded
            self.downloads[download_id]['progress'].total_size = total_size
            
            # Notify all callbacks with the current progress
            for callback in self.callbacks:
                callback(download_id, self.downloads[download_id]['progress'])

        # Mark download as complete
        self.downloads[download_id]['progress'].status = DownloadStatus.COMPLETED
        for callback in self.callbacks:
            callback(download_id, self.downloads[download_id]['progress'])
