"""Main backup orchestration logic."""
import os
import datetime
import shutil
from typing import List
from config import Config
from telegram_logger import TelegramLogger
from compressor import Compressor
from uploader import NextcloudUploader


class BackupManager:
    """Orchestrate the backup process."""
    
    def __init__(self):
        """Initialize backup manager with dependencies."""
        self.logger = TelegramLogger()
        self.uploader = NextcloudUploader(self.logger)
        self.compressor = Compressor()
    
    def get_backup_directories(self) -> List[str]:
        """
        Get list of directories to backup (excluding blacklisted ones).
        
        Returns:
            List of absolute directory paths to backup
        """
        base_dir = Config.BACKUP_BASE_DIR
        forbidden_file = Config.FORBIDDEN_DIRS_FILE
        
        # Load blacklist
        blacklist = set()
        if os.path.exists(forbidden_file):
            try:
                with open(forbidden_file, "r") as f:
                    blacklist = {
                        os.path.abspath(line.strip())
                        for line in f.readlines()
                        if line.strip()
                    }
            except Exception as e:
                self.logger.send_error(f"Failed to read forbidden file: {e}")
        
        # Get all directories
        directories = []
        try:
            for item in os.listdir(base_dir):
                full_path = os.path.abspath(os.path.join(base_dir, item))
                if os.path.isdir(full_path) and full_path not in blacklist:
                    directories.append(full_path)
        except Exception as e:
            self.logger.send_error(f"Failed to list directories: {e}")
        
        return sorted(directories)
    
    def run_backup(self) -> None:
        """Execute the complete backup process."""
        self.logger.send("🚀 Starting backup process...")
        
        # Create timestamp for this backup session
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        work_dir = os.path.abspath(timestamp)
        os.makedirs(work_dir, exist_ok=True)
        
        try:
            # Get directories to backup
            directories = self.get_backup_directories()
            total_dirs = len(directories)
            
            if total_dirs == 0:
                self.logger.send_info("No directories found for backup.")
                return
            
            self.logger.send(
                f"📂 Found {total_dirs} director{'y' if total_dirs == 1 else 'ies'} for backup"
            )
            
            # Process each directory
            total_successful = 0
            total_failed = 0
            
            for idx, directory in enumerate(directories, start=1):
                dir_name = os.path.basename(directory)
                
                # Calculate and log directory size
                dir_size = self.compressor.get_directory_size(directory)
                size_str = self.compressor.format_size(dir_size)
                
                self.logger.send(
                    f"📦 [{idx}/{total_dirs}] Compressing: {dir_name} ({size_str})"
                )
                
                try:
                    # Compress directory
                    archive_parts = self.compressor.compress_directory(
                        directory, work_dir
                    )
                    
                    # Log compression results with file sizes
                    total_size = sum(os.path.getsize(f) for f in archive_parts)
                    size_str = self.compressor.format_size(total_size)
                    self.logger.send(
                        f"✅ Compressed into {len(archive_parts)} part(s) ({size_str} total)"
                    )
                    
                    # Upload parts
                    remote_path = f"{Config.NEXTCLOUD_BACKUP_PATH}/{timestamp}"
                    successful, failed = self.uploader.upload_files_parallel(
                        archive_parts, remote_path, dir_name
                    )
                    
                    total_successful += successful
                    total_failed += failed
                    
                    if failed == 0:
                        self.logger.send_success(
                            f"Completed {dir_name}: {successful} part(s) uploaded"
                        )
                    else:
                        self.logger.send_error(
                            f"Completed {dir_name} with errors: "
                            f"{successful} succeeded, {failed} failed"
                        )
                    
                except Exception as e:
                    self.logger.send_error(f"Failed to backup {dir_name}: {e}")
                    total_failed += 1
                
                # Clean up work directory after each backup to save disk space
                try:
                    shutil.rmtree(work_dir, ignore_errors=True)
                    os.makedirs(work_dir, exist_ok=True)
                except Exception as e:
                    self.logger.send_error(f"Failed to clean work directory: {e}")
            
            # Final summary
            self.logger.send(
                f"🎉 Backup process completed!\n"
                f"Total uploads: {total_successful} succeeded, {total_failed} failed"
            )
            
        except Exception as e:
            self.logger.send_error(f"Backup process error: {e}")
        
        finally:
            # Final cleanup
            try:
                shutil.rmtree(work_dir, ignore_errors=True)
            except Exception:
                pass

