"""Telegram logging functionality."""
import requests
from typing import Optional
from config import Config


class TelegramLogger:
    """Send log messages to Telegram channel."""
    
    def __init__(self):
        """Initialize Telegram logger with config."""
        self.token = Config.TELEGRAM_TOKEN
        self.channel_id = Config.TELEGRAM_CHANNEL_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def send(self, text: str, silent: bool = False) -> bool:
        """
        Send a message to Telegram channel.
        
        Args:
            text: Message text to send
            silent: If True, send without notification
            
        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/sendMessage"
            params = {
                "chat_id": self.channel_id,
                "text": text,
                "disable_notification": silent
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to send Telegram message: {text} | Error: {e}")
            return False
    
    def send_error(self, text: str) -> bool:
        """Send error message with emoji."""
        return self.send(f"❌ {text}")
    
    def send_success(self, text: str) -> bool:
        """Send success message with emoji."""
        return self.send(f"✅ {text}")
    
    def send_info(self, text: str) -> bool:
        """Send info message with emoji."""
        return self.send(f"ℹ️ {text}")
    
    def send_progress(self, text: str) -> bool:
        """Send progress message with emoji."""
        return self.send(f"⏳ {text}", silent=True)

