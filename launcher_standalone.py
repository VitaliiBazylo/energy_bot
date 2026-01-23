"""
EnergyBot Standalone Launcher - Повністю автономний запуск
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import sys
import threading
import json
from pathlib import Path
import asyncio
import logging
from io import StringIO

class TextHandler(logging.Handler):
    """Обробник для виводу логів в GUI"""
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)

class EnergyBotLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("EnergyBot Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Шляхи
        if getattr(sys, 'frozen', False):
            # Запущено як EXE
            self.project_dir = Path(sys.executable).parent
        else:
            # Запущено як Python скрипт
            self.project_dir = Path(__file__).parent
            
        self.env_file = self.project_dir / ".env"
        self.cameras_file = self.project_dir / "cameras.json"
        
        self.bot_thread = None
        self.bot_running = False
        
        # Створення інтерфейсу
        self.create_widgets()
        self.check_setup()
        
    def create_widgets(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg="#2196F3", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="⚡ EnergyBot Launcher", 
                              font=("Arial", 18, "bold"), bg="#2196F3", fg="white")
        title_label.pack(pady=15)
        
        # Статус
        status_frame = tk.Frame(self.root, padx=20, pady=10)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(status_frame, text="Статус: Не запущено", 
                                     font=("Arial", 11), fg="red")
        self.status_label.pack()
        
        # Кнопки управління
        button_frame = tk.Frame(self.root, padx=20, pady=10)
        button_frame.pack()
        
        self.start_btn = tk.Button(button_frame, text="▶ Запустити", 
                                   command=self.start_bot, bg="#4CAF50", fg="white",
                                   font=("Arial", 10, "bold"), width=15, height=2)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="⏹ Зупинити", 
                                  command=self.stop_bot, bg="#f44336", fg="white",
                                  font=("Arial", 10, "bold"), width=15, height=2, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        # Кнопки налаштувань
        settings_frame = tk.Frame(self.root, padx=20, pady=5)
        settings_frame.pack()
        
        tk.Button(settings_frame, text="⚙ Налаштування (.env)", 
                 command=self.edit_env, width=20).grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(settings_frame, text="📹 Камери (cameras.json)", 
                 command=self.edit_cameras, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(settings_frame, text="🔄 Перевірити налаштування", 
                 command=self.check_setup, width=20).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Логи
        log_frame = tk.LabelFrame(self.root, text="📝 Логи", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, 
                                                  font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Налаштування логування
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_handler)
        logging.getLogger().setLevel(logging.INFO)
        
    def log(self, message, level="INFO"):
        """Додати повідомлення в лог"""
        if level == "INFO":
            logging.info(message)
        elif level == "ERROR":
            logging.error(message)
        elif level == "WARNING":
            logging.warning(message)
        else:
            logging.info(message)
        
    def check_setup(self):
        """Перевірка налаштувань"""
        self.log("Перевірка налаштувань...", "INFO")
        
        # Перевірка .env
        if not self.env_file.exists():
            self.log("⚠️ Файл .env не знайдено!", "WARNING")
            messagebox.showwarning("Увага", "Файл .env не знайдено!\nНатисніть 'Налаштування (.env)' для створення")
            return False
            
        # Перевірка cameras.json
        if not self.cameras_file.exists():
            self.log("⚠️ Файл cameras.json не знайдено!", "WARNING")
            messagebox.showwarning("Увага", "Файл cameras.json не знайдено!\nНатисніть 'Камери' для створення")
            return False
            
        self.log("✅ Налаштування коректні", "INFO")
        return True
        
    def start_bot(self):
        """Запуск бота"""
        if not self.check_setup():
            return
            
        if self.bot_running:
            messagebox.showinfo("Інфо", "Бот вже запущено!")
            return
            
        self.log("🚀 Запуск бота...", "INFO")
        
        try:
            self.bot_running = True
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            
            self.status_label.config(text="Статус: ✅ Запущено", fg="green")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.log("✅ Бот запущено!", "INFO")
            
        except Exception as e:
            self.log(f"❌ Помилка запуску: {e}", "ERROR")
            messagebox.showerror("Помилка", f"Не вдалося запустити бота:\n{e}")
            self.bot_running = False
            
    def run_bot(self):
        """Запуск бота в окремому потоці"""
        try:
            # Імпорт модулів бота
            sys.path.insert(0, str(self.project_dir))
            
            from main import main as bot_main
            
            # Запуск бота
            asyncio.run(bot_main())
            
        except Exception as e:
            self.log(f"❌ Помилка виконання бота: {e}", "ERROR")
        finally:
            self.bot_running = False
            self.root.after(0, self.on_bot_stopped)
            
    def on_bot_stopped(self):
        """Обробка зупинки бота"""
        self.status_label.config(text="Статус: ⭕ Зупинено", fg="red")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
            
    def stop_bot(self):
        """Зупинка бота"""
        if not self.bot_running:
            return
            
        self.log("🛑 Зупинка бота...", "INFO")
        
        # Зупинка asyncio
        self.bot_running = False
        
        self.log("✅ Бот зупинено", "INFO")
        self.on_bot_stopped()
        
    def edit_env(self):
        """Редагування .env"""
        if not self.env_file.exists():
            # Створити з прикладу
            default_env = """# Токен Telegram бота (отримайте у @BotFather)
BOT_TOKEN=your_bot_token_here

# Chat ID користувачів (через кому)
CHAT_IDS=123456789,987654321
"""
            self.env_file.write_text(default_env, encoding='utf-8')
            
        os.startfile(str(self.env_file))
        self.log("📝 Відкрито .env для редагування", "INFO")
        
    def edit_cameras(self):
        """Редагування cameras.json"""
        if not self.cameras_file.exists():
            # Створити приклад
            example_data = [{"name": "Hikvision Camera", "ip": "192.168.1.195"}]
            self.cameras_file.write_text(json.dumps(example_data, indent=2, ensure_ascii=False), encoding='utf-8')
            
        os.startfile(str(self.cameras_file))
        self.log("📝 Відкрито cameras.json для редагування", "INFO")

def main():
    root = tk.Tk()
    app = EnergyBotLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
