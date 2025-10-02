"""Nextcloud upload functionality."""
import os
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import nextcloud_client
from config import Config
from telegram_logger import TelegramLogger


class NextcloudUploader:
    """Handle file uploads to Nextcloud."""
    
    def __init__(self, logger: TelegramLogger):
        """Initialize uploader with Nextcloud credentials."""
        self.base_url = Config.NEXTCLOUD_URL
        self.username = Config.NEXTCLOUD_USERNAME
        self.password = Config.NEXTCLOUD_PASSWORD
        self.logger = logger
    
    def upload_file(self, local_file: str, remote_directory: str) -> None:
        """
        Upload a single file to Nextcloud.
        
        Args:
            local_file: Path to local file
            remote_directory: Remote directory path in Nextcloud
            
        Raises:
            Exception: If upload fails
        """
        nc = nextcloud_client.Client(self.base_url)
        nc.login(self.username, self.password)
        
        # Ensure remote directory exists
        try:
            nc.mkdir(remote_directory)
        except Exception:
            pass  # Directory probably exists
        
        filename = os.path.basename(local_file)
        remote_path = os.path.join(remote_directory, filename)
        nc.put_file(remote_path, local_file)
    
    def upload_files_parallel(
        self,
        files: List[str],
        remote_directory: str,
        dir_name: str = ""
    ) -> tuple[int, int]:
        """
        Upload multiple files in parallel using thread pool.
        
        Args:
            files: List of local file paths
            remote_directory: Remote directory path in Nextcloud
            dir_name: Directory name for logging
            
        Returns:
            Tuple of (successful_uploads, failed_uploads)
        """
        successful = 0
        failed = 0
        total = len(files)
        
        self.logger.send_progress(
            f"⬆️ Uploading {total} part(s) for {dir_name} in parallel..."
        )
        
        with ThreadPoolExecutor(max_workers=Config.MAX_UPLOAD_WORKERS) as executor:
            # Submit all upload tasks
            future_to_file = {
                executor.submit(self.upload_file, file, remote_directory): file
                for file in files
            }
            
            # Process completed uploads
            for idx, future in enumerate(as_completed(future_to_file), start=1):
                file_path = future_to_file[future]
                filename = os.path.basename(file_path)
                
                try:
                    future.result()
                    successful += 1
                    self.logger.send(
                        f"✅ Uploaded {idx}/{total}: {filename}",
                        silent=True
                    )
                except Exception as e:
                    failed += 1
                    self.logger.send_error(
                        f"Failed to upload {filename}: {str(e)}"
                    )
        
        return successful, failed

