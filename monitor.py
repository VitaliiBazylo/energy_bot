"""
Модуль моніторингу камер
"""
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Set
import platform
import subprocess

logger = logging.getLogger(__name__)


class CameraMonitor:
    """Клас для моніторингу камер через пінг"""
    
    def __init__(self, cameras: List[Dict[str, str]], bot, chat_ids: List[int]):
        self.cameras = cameras
        self.bot = bot
        self.chat_ids = chat_ids
        self.camera_status: Dict[str, bool] = {}  # True = онлайн, False = офлайн
        self.last_check: Dict[str, datetime] = {}
        self.initial_check_done = False  # Прапорець першої перевірки
    
    async def ping_camera(self, ip: str, timeout: int = 5, count: int = 3) -> bool:
        """
        Перевіряє доступність камери через TCP порт 8000
        """
        try:
            # Перевірка доступності порту 8000
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, 8000),
                timeout=timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False
        except Exception as e:
            logger.error(f"Помилка при перевірці {ip}:8000: {e}")
            return False
    
    async def check_camera(self, camera: Dict[str, str]) -> None:
        """Перевіряє одну камеру та відправляє сповіщення при зміні статусу"""
        ip = camera['ip']
        name = camera['name']
        
        # Пінгування камери
        is_online = await self.ping_camera(ip)
        
        # Отримання попереднього статусу (None при першій перевірці)
        was_online = self.camera_status.get(ip)
        
        # Оновлення часу перевірки
        self.last_check[ip] = datetime.now()
        
        # Якщо це перша перевірка - просто зберігаємо статус без сповіщення
        if was_online is None:
            self.camera_status[ip] = is_online
            logger.info(f"Початковий стан {name} ({ip}): {'онлайн' if is_online else 'офлайн'}")
            return
        
        # Якщо статус змінився - відправити сповіщення
        if is_online != was_online:
            self.camera_status[ip] = is_online
            
            if is_online:
                # Камера з'явилась онлайн - світло включили
                message = f"🟢 ⚡ Світло Є\n🕐 {datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}"
                logger.info(f"Світло включено: {name} ({ip})")
            else:
                # Камера пішла офлайн - світло вимкнули
                message = f"🔴 🔌 Світла немає\n🕐 {datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}"
                logger.warning(f"Світло вимкнено: {name} ({ip})")
            
            # Відправка сповіщення всім підписаним чатам
            for chat_id in self.chat_ids:
                try:
                    await self.bot.send_message(chat_id, message)
                except Exception as e:
                    logger.error(f"Помилка відправки повідомлення до {chat_id}: {e}")
    
    async def start_monitoring(self, interval: int = 60) -> None:
        """
        Запуск циклу моніторингу
        :param interval: Інтервал перевірки в секундах
        """
        logger.info(f"Початок моніторингу {len(self.cameras)} камер (інтервал: {interval}с)")
        
        while True:
            try:
                # Перевірка всіх камер паралельно
                tasks = [self.check_camera(camera) for camera in self.cameras]
                await asyncio.gather(*tasks)
                
                # Очікування до наступної перевірки
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                logger.info("Моніторинг зупинено")
                break
            except Exception as e:
                logger.error(f"Помилка в циклі моніторингу: {e}")
                await asyncio.sleep(interval)
    
    def get_status_report(self) -> str:
        """Формує звіт про поточний стан камер"""
        # Беремо першу камеру (у нас одна)
        if self.cameras:
            camera = self.cameras[0]
            ip = camera['ip']
            is_online = self.camera_status.get(ip, False)
            last_check = self.last_check.get(ip)
            
            if is_online:
                status = "🟢 ⚡ Світло Є"
            else:
                status = "🔴 🔌 Світла немає"
            
            report = f"📊 Статус:\n{status}"
            if last_check:
                report += f"\n🕐 {last_check.strftime('%H:%M:%S')}"
            
            return report
        
        return "❌ Немає камер для моніторингу"
