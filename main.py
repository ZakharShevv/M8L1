import tkinter as tk
from tkinter import messagebox
from challenges import get_challenges
from db import init_db, mark_completed, get_completed, get_total_points

class EcoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌍 Экологические Челленджи")
        self.root.geometry("600x700")

        self.title = tk.Label(
            root,
            text="Добро пожаловать в Эко-Челлендж!",
            font=("Arial", 18, "bold"),
            fg="green"
        )
        self.title.pack(pady=20)

        self.instructions = tk.Label(
            root,
            text="Выбери одно или несколько заданий и начни спасать планету 🌱",
            font=("Arial", 12)
        )
        self.instructions.pack(pady=10)

        # Вставленный код для отображения очков
        self.points_label = tk.Label(
            root,
            text=f"Твои очки: {get_total_points()}",
            font=("Arial", 12, "bold"),
            fg="blue"
        )
        self.points_label.pack(pady=10)

        self.challenge_frame = tk.LabelFrame(root, text="💪 Доступные Челленджи", padx=10, pady=10)
        self.challenge_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_button = tk.Button(
            root,
            text="🔁 Обновить список заданий",
            font=("Arial", 12),
            command=self.update_challenges
        )
        self.refresh_button.pack(pady=10)

        self.footer = tk.Label(
            root,
            text="Сделано с заботой об экологии 🌏",
            font=("Arial", 10),
            fg="gray"
        )
        
        self.footer.pack(side="bottom", pady=10)

        self.selected_challenge = None
        self.confirm_button = None

        self.update_challenges()

    def update_challenges(self):
        for widget in self.challenge_frame.winfo_children():
            widget.destroy()

        challenges = get_challenges()
        completed = get_completed()

        for task in challenges:
            frame = tk.Frame(self.challenge_frame)
            frame.pack(pady=5, fill="x")

            if task in completed:
                btn = tk.Button(
                    frame,
                    text=f"✅ {task}",
                    font=("Arial", 11),
                    width=40,
                    state="disabled",
                    disabledforeground="gray"
                )
            else:
                btn = tk.Button(
                    frame,
                    text=task,
                    font=("Arial", 11),
                    width=40,
                    command=lambda t=task, f=frame: self.show_confirm_button(t, f)
                )
            btn.pack()


    def show_confirm_button(self, challenge_text, parent_frame):
        if self.confirm_button:
            self.confirm_button.destroy()

        self.selected_challenge = challenge_text
        self.confirm_button = tk.Button(
            parent_frame,
            text="✅ Выполнить",
            font=("Arial", 10),
            bg="lightgreen",
            command=self.confirm_challenge
        )
        self.confirm_button.pack(pady=3)

    def confirm_challenge(self):
        if self.selected_challenge:
            mark_completed(self.selected_challenge, points=10)
            messagebox.showinfo(
                "Успех!",
                f"Вы выполнили задание:\n\n{self.selected_challenge}\n\n+10 очков!"
            )
            self.selected_challenge = None
            if self.confirm_button:
                self.confirm_button.destroy()
                self.confirm_button = None
            self.update_challenges()
            self.points_label.config(text=f"Твои очки: {get_total_points()}")


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = EcoApp(root)
    root.mainloop()

