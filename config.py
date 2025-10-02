"""Configuration management for Nextcloud Backuper."""
import os
from typing import Optional


class Config:
    """Application configuration loaded from environment variables."""
    
    # Nextcloud Configuration
    NEXTCLOUD_URL: str
    NEXTCLOUD_USERNAME: str
    NEXTCLOUD_PASSWORD: str
    NEXTCLOUD_BACKUP_PATH: str
    
    # Telegram Configuration
    TELEGRAM_TOKEN: str
    TELEGRAM_CHANNEL_ID: str
    
    # Backup Configuration
    BACKUP_BASE_DIR: str
    FORBIDDEN_DIRS_FILE: str
    MAX_VOLUME_SIZE: int  # in bytes
    MAX_UPLOAD_WORKERS: int
    COMPRESSION_PRESET: int  # 0-9, lower=faster
    USE_MULTIPROCESSING: bool  # Enable multi-core compression
    
    # Schedule Configuration
    BACKUP_HOUR: int
    BACKUP_MINUTE: int
    TIMEZONE: str
    RUN_ON_STARTUP: bool
    
    @classmethod
    def load(cls) -> None:
        """Load configuration from environment variables."""
        # Nextcloud (required)
        cls.NEXTCLOUD_URL = cls._get_required_env("NEXTCLOUD_URL")
        cls.NEXTCLOUD_USERNAME = cls._get_required_env("NEXTCLOUD_USERNAME")
        cls.NEXTCLOUD_PASSWORD = cls._get_required_env("NEXTCLOUD_PASSWORD")
        cls.NEXTCLOUD_BACKUP_PATH = os.getenv("NEXTCLOUD_BACKUP_PATH", "backup/mainserver")
        
        # Telegram (required)
        cls.TELEGRAM_TOKEN = cls._get_required_env("TELEGRAM_TOKEN")
        cls.TELEGRAM_CHANNEL_ID = cls._get_required_env("TELEGRAM_CHANNEL_ID")
        
        # Backup settings
        cls.BACKUP_BASE_DIR = os.getenv("BACKUP_BASE_DIR", ".")
        cls.FORBIDDEN_DIRS_FILE = os.getenv("FORBIDDEN_DIRS_FILE", "forbidden")
        cls.MAX_VOLUME_SIZE = int(os.getenv("MAX_VOLUME_SIZE", str(1024 * 1024 * 1024)))  # 1GB default
        cls.MAX_UPLOAD_WORKERS = int(os.getenv("MAX_UPLOAD_WORKERS", "4"))
        cls.COMPRESSION_PRESET = int(os.getenv("COMPRESSION_PRESET", "1"))  # 1 = very fast (recommended)
        cls.USE_MULTIPROCESSING = os.getenv("USE_MULTIPROCESSING", "true").lower() == "true"
        
        # Schedule settings
        cls.BACKUP_HOUR = int(os.getenv("BACKUP_HOUR", "3"))
        cls.BACKUP_MINUTE = int(os.getenv("BACKUP_MINUTE", "0"))
        cls.TIMEZONE = os.getenv("TIMEZONE", "America/New_York")  # EDT/EST
        cls.RUN_ON_STARTUP = os.getenv("RUN_ON_STARTUP", "true").lower() == "true"
    
    @staticmethod
    def _get_required_env(key: str) -> str:
        """Get required environment variable or raise error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable '{key}' is not set")
        return value
    
    @classmethod
    def validate(cls) -> None:
        """Validate configuration values."""
        if not cls.NEXTCLOUD_URL.startswith(("http://", "https://")):
            raise ValueError("NEXTCLOUD_URL must start with http:// or https://")
        
        if cls.MAX_VOLUME_SIZE <= 0:
            raise ValueError("MAX_VOLUME_SIZE must be positive")
        
        if cls.MAX_UPLOAD_WORKERS <= 0:
            raise ValueError("MAX_UPLOAD_WORKERS must be positive")
        
        if not (0 <= cls.COMPRESSION_PRESET <= 9):
            raise ValueError("COMPRESSION_PRESET must be between 0 and 9")
        
        if not (0 <= cls.BACKUP_HOUR <= 23):
            raise ValueError("BACKUP_HOUR must be between 0 and 23")
        
        if not (0 <= cls.BACKUP_MINUTE <= 59):
            raise ValueError("BACKUP_MINUTE must be between 0 and 59")

