"""Directory compression functionality."""
import os
from typing import List
import multivolumefile
import py7zr
from config import Config


class Compressor:
    """Handle directory compression into multi-volume 7z archives."""
    
    @staticmethod
    def compress_directory(
        directory_path: str,
        output_path: str,
        max_size: int = None
    ) -> List[str]:
        """
        Compress a directory into multi-volume .7z files.
        
        Args:
            directory_path: Path to directory to compress
            output_path: Output directory for compressed files
            max_size: Maximum volume size in bytes (default from config)
            
        Returns:
            List of paths to generated archive files
            
        Raises:
            ValueError: If directory_path is not a valid directory
        """
        if not os.path.isdir(directory_path):
            raise ValueError(f"Path '{directory_path}' is not a valid directory")
        
        if max_size is None:
            max_size = Config.MAX_VOLUME_SIZE
        
        os.makedirs(output_path, exist_ok=True)
        
        dir_name = os.path.basename(directory_path)
        archive_path = os.path.join(output_path, f"{dir_name}.7z")
        
        # Create multi-volume 7z archive
        with multivolumefile.open(archive_path, mode="wb", volume=max_size) as target:
            with py7zr.SevenZipFile(target, mode='w') as archive:
                archive.writeall(directory_path, arcname=dir_name)
        
        # Return sorted list of generated files
        archive_files = [
            os.path.join(output_path, f)
            for f in sorted(os.listdir(output_path))
            if f.startswith(dir_name)
        ]
        
        # Verify files were created
        for file in archive_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Expected archive file not found: {file}")
            size = os.path.getsize(file)
            if size == 0:
                raise ValueError(f"Archive file is empty (0 bytes): {file}")
        
        return archive_files
    
    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """
        Calculate total size of directory in bytes.
        
        Args:
            directory_path: Path to directory
            
        Returns:
            Total size in bytes
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.isfile(filepath):
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, PermissionError):
                        pass  # Skip files we can't access
        return total_size
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format bytes to human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

