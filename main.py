#!/usr/bin/env python3
"""Main entry point for Nextcloud Backuper."""
import datetime
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from config import Config
from backup_manager import BackupManager
from telegram_logger import TelegramLogger


def main():
    """Main function to initialize and run the backup scheduler."""
    try:
        # Load and validate configuration
        Config.load()
        Config.validate()
        
        # Initialize logger
        logger = TelegramLogger()
        logger.send("🔄 Backuper started and scheduler initialized.")
        
        # Initialize backup manager
        backup_manager = BackupManager()
        
        # Setup scheduler
        timezone = pytz.timezone(Config.TIMEZONE)
        scheduler = BlockingScheduler(timezone=timezone)
        
        # Add scheduled job
        scheduler.add_job(
            backup_manager.run_backup,
            "cron",
            hour=Config.BACKUP_HOUR,
            minute=Config.BACKUP_MINUTE,
            id="daily_backup"
        )
        
        logger.send(
            f"⏰ Scheduled daily backup at "
            f"{Config.BACKUP_HOUR:02d}:{Config.BACKUP_MINUTE:02d} {Config.TIMEZONE}"
        )
        
        # Run immediately on startup if configured
        if Config.RUN_ON_STARTUP:
            logger.send("▶️ Running immediate backup on startup...")
            backup_manager.run_backup()
            logger.send("✅ Initial backup completed. Scheduler will now take over.")
        
        # Start scheduler (blocking)
        scheduler.start()
        
    except KeyboardInterrupt:
        logger = TelegramLogger()
        logger.send("⏹️ Backuper stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        try:
            logger = TelegramLogger()
            logger.send_error(f"Fatal error: {e}")
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()

