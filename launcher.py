"""
EnergyBot Launcher - Графічний інтерфейс для управління ботом
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import os
import sys
import threading
import json
from pathlib import Path

class EnergyBotLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("EnergyBot Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Шляхи
        self.project_dir = Path(__file__).parent
        self.python_exe = self.project_dir / ".venv" / "Scripts" / "python.exe"
        self.main_py = self.project_dir / "main.py"
        self.env_file = self.project_dir / ".env"
        self.cameras_file = self.project_dir / "cameras.json"
        
        self.bot_process = None
        
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
        
        tk.Button(settings_frame, text="📋 Отримати Chat ID", 
                 command=self.get_chat_id, width=20).grid(row=1, column=0, padx=5, pady=5)
        
        tk.Button(settings_frame, text="🔄 Перевірити налаштування", 
                 command=self.check_setup, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # Логи
        log_frame = tk.LabelFrame(self.root, text="📝 Логи", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, 
                                                  font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def log(self, message, level="INFO"):
        """Додати повідомлення в лог"""
        colors = {"INFO": "black", "ERROR": "red", "SUCCESS": "green", "WARNING": "orange"}
        self.log_text.insert(tk.END, f"[{level}] {message}\n")
        self.log_text.see(tk.END)
        
    def check_setup(self):
        """Перевірка налаштувань"""
        self.log("Перевірка налаштувань...", "INFO")
        
        # Перевірка Python
        if not self.python_exe.exists():
            self.log("❌ Віртуальне оточення не знайдено! Запустіть setup.bat", "ERROR")
            messagebox.showerror("Помилка", "Віртуальне оточення не знайдено!\nЗапустіть setup.bat")
            return False
            
        # Перевірка .env
        if not self.env_file.exists():
            self.log("⚠️ Файл .env не знайдено!", "WARNING")
            messagebox.showwarning("Увага", "Файл .env не знайдено!\nНатисніть 'Налаштування (.env)' для створення")
            return False
            
        # Перевірка cameras.json
        if not self.cameras_file.exists():
            self.log("⚠️ Файл cameras.json не знайдено!", "WARNING")
            return False
            
        self.log("✅ Налаштування коректні", "SUCCESS")
        return True
        
    def start_bot(self):
        """Запуск бота"""
        if not self.check_setup():
            return
            
        if self.bot_process:
            messagebox.showinfo("Інфо", "Бот вже запущено!")
            return
            
        self.log("🚀 Запуск бота...", "INFO")
        
        try:
            # Запуск бота в окремому потоці
            self.bot_process = subprocess.Popen(
                [str(self.python_exe), str(self.main_py)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=str(self.project_dir)
            )
            
            # Читання виводу в окремому потоці
            threading.Thread(target=self.read_output, daemon=True).start()
            
            self.status_label.config(text="Статус: ✅ Запущено", fg="green")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.log("✅ Бот запущено!", "SUCCESS")
            
        except Exception as e:
            self.log(f"❌ Помилка запуску: {e}", "ERROR")
            messagebox.showerror("Помилка", f"Не вдалося запустити бота:\n{e}")
            
    def stop_bot(self):
        """Зупинка бота"""
        if not self.bot_process:
            return
            
        self.log("🛑 Зупинка бота...", "INFO")
        
        try:
            self.bot_process.terminate()
            self.bot_process.wait(timeout=5)
        except:
            self.bot_process.kill()
            
        self.bot_process = None
        self.status_label.config(text="Статус: ⭕ Зупинено", fg="red")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        self.log("✅ Бот зупинено", "SUCCESS")
        
    def read_output(self):
        """Читання виводу бота"""
        try:
            for line in iter(self.bot_process.stdout.readline, ''):
                if line:
                    self.log_text.insert(tk.END, line)
                    self.log_text.see(tk.END)
        except:
            pass
            
    def edit_env(self):
        """Редагування .env"""
        if not self.env_file.exists():
            # Створити з прикладу
            example = self.project_dir / ".env.example"
            if example.exists():
                self.env_file.write_text(example.read_text())
                
        os.startfile(str(self.env_file))
        self.log("📝 Відкрито .env для редагування", "INFO")
        
    def edit_cameras(self):
        """Редагування cameras.json"""
        if not self.cameras_file.exists():
            # Створити приклад
            example_data = [{"name": "Hikvision Camera", "ip": "192.168.1.195"}]
            self.cameras_file.write_text(json.dumps(example_data, indent=2, ensure_ascii=False))
            
        os.startfile(str(self.cameras_file))
        self.log("📝 Відкрито cameras.json для редагування", "INFO")
        
    def get_chat_id(self):
        """Отримання Chat ID"""
        get_chat_id_py = self.project_dir / "get_chat_id.py"
        if not get_chat_id_py.exists():
            messagebox.showerror("Помилка", "Файл get_chat_id.py не знайдено!")
            return
            
        self.log("🔍 Запуск get_chat_id.py...", "INFO")
        subprocess.Popen([str(self.python_exe), str(get_chat_id_py)], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE)

def main():
    root = tk.Tk()
    app = EnergyBotLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
