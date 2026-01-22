"""
Конфігурація бота
"""
import os
from typing import List, Dict
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()


class Config:
    """Клас конфігурації"""
    
    def __init__(self):
        # Токен телеграм бота
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не знайдено в .env файлі!")
        
        # ID чатів для отримання сповіщень (розділені комами)
        chat_ids = os.getenv("CHAT_IDS", "")
        self.CHAT_IDS = [int(chat_id.strip()) for chat_id in chat_ids.split(",") if chat_id.strip()]
        
        if not self.CHAT_IDS:
            raise ValueError("CHAT_IDS не знайдено в .env файлі!")
        
        # Налаштування моніторингу
        self.PING_INTERVAL = int(os.getenv("PING_INTERVAL", "60"))  # Інтервал перевірки в секундах
        self.PING_TIMEOUT = int(os.getenv("PING_TIMEOUT", "5"))  # Таймаут пінгу в секундах
        self.PING_COUNT = int(os.getenv("PING_COUNT", "3"))  # Кількість спроб пінгу
        
        # Камери для моніторингу (завантажуються з cameras.json)
        self.CAMERAS = self._load_cameras()
    
    def _load_cameras(self) -> List[Dict[str, str]]:
        """Завантаження списку камер з файлу"""
        import json
        from pathlib import Path
        
        cameras_file = Path("cameras.json")
        if not cameras_file.exists():
            # Створення файлу з прикладом
            example_cameras = [
                {
                    "name": "Камера 1",
                    "ip": "192.168.1.100"
                },
                {
                    "name": "Камера 2",
                    "ip": "192.168.1.101"
                }
            ]
            with open(cameras_file, "w", encoding="utf-8") as f:
                json.dump(example_cameras, f, ensure_ascii=False, indent=2)
            return example_cameras
        
        with open(cameras_file, "r", encoding="utf-8") as f:
            return json.load(f)
