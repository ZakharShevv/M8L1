import tkinter as tk
from tkinter import messagebox
from db import init_db, mark_completed, get_completed, get_total_points
from challenges import get_challenges

class EcoAppTemplate:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.selected_challenge = None
        self.confirm_button = None
        self.update_challenges()
    
    def setup_window(self):
        self.root.title("🌍 Экологические Челленджи")
        self.root.geometry("600x700")
    
    def create_widgets(self):
        # Заголовок
        tk.Label(
            self.root,
            text="Добро пожаловать в Эко-Челлендж!",
            font=("Arial", 18, "bold"),
            fg="green"
        ).pack(pady=20)
        
        # Инструкция
        tk.Label(
            self.root,
            text="Выбери одно или несколько заданий и начни спасать планету 🌱",
            font=("Arial", 12)
        ).pack(pady=10)
        
        # Очки
        self.points_label = tk.Label(
            self.root,
            text=f"Твои очки: {get_total_points()}",
            font=("Arial", 12, "bold"),
            fg="blue"
        )
        self.points_label.pack(pady=10)
        
        # Фрейм для заданий
        self.challenge_frame = tk.LabelFrame(
            self.root, 
            text="💪 Доступные Челленджи", 
            padx=10, 
            pady=10
        )
        self.challenge_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Кнопка обновления
        tk.Button(
            self.root,
            text="🔁 Обновить список заданий",
            font=("Arial", 12),
            command=self.update_challenges
        ).pack(pady=10)
        
        # Подвал
        tk.Label(
            self.root,
            text="Сделано с заботой об экологии 🌏",
            font=("Arial", 10),
            fg="gray"
        ).pack(side="bottom", pady=10)
    
    def update_challenges(self):
        for widget in self.challenge_frame.winfo_children():
            widget.destroy()
        
        for task in get_challenges():
            frame = tk.Frame(self.challenge_frame)
            frame.pack(pady=5, fill="x")
            
            if task in get_completed():
                btn = tk.Button(
                    frame,
                    text=f"✅ {task}",
                    font=("Arial", 11),
                    width=40,
                    state="disabled"
                )
            else:
                btn = tk.Button(
                    frame,
                    text=task,
                    font=("Arial", 11),
                    width=40,
                    command=lambda t=task, f=frame: self.select_challenge(t, f)
                )
            btn.pack()
    
    def select_challenge(self, challenge, frame):
        if self.confirm_button:
            self.confirm_button.destroy()
        
        self.selected_challenge = challenge
        self.confirm_button = tk.Button(
            frame,
            text="✅ Выполнить",
            bg="lightgreen",
            command=self.confirm_challenge
        )
        self.confirm_button.pack(pady=3)
    
    def confirm_challenge(self):
        if not self.selected_challenge:
            return
            
        mark_completed(self.selected_challenge, points=10)
        messagebox.showinfo("Успех!", f"Выполнено: {self.selected_challenge}\n+10 очков!")
        
        self.selected_challenge = None
        if self.confirm_button:
            self.confirm_button.destroy()
            self.confirm_button = None
        
        self.update_challenges()
        self.points_label.config(text=f"Твои очки: {get_total_points()}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = EcoAppTemplate(root)
    root.mainloop()
