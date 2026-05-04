import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = 'training_data.json'

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Создаем рамки и компоненты
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky='w')
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, sticky='ew')

        ttk.Label(frame, text="Тип тренировки:").grid(row=1, column=0, sticky='w')
        self.type_entry = ttk.Entry(frame)
        self.type_entry.grid(row=1, column=1, sticky='ew')

        ttk.Label(frame, text="Длительность (мин):").grid(row=2, column=0, sticky='w')
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=2, column=1, sticky='ew')

        # Кнопка добавления
        add_btn = ttk.Button(frame, text="Добавить тренировку", command=self.add_training)
        add_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # Настройка растягиваемости колонок
        frame.columnconfigure(1, weight=1)

        # Таблица для отображения тренировок
        self.tree = ttk.Treeview(self.root, columns=('date', 'type', 'duration'), show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип тренировки')
        self.tree.heading('duration', text='Длительность')
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Фильтр
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(padx=10, pady=5, fill='x')

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0)
        self.filter_type_var = tk.StringVar()
        self.filter_type_entry = ttk.Entry(filter_frame, textvariable=self.filter_type_var)
        self.filter_type_entry.grid(row=0, column=1)

        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=2)
        self.filter_date_var = tk.StringVar()
        self.filter_date_entry = ttk.Entry(filter_frame, textvariable=self.filter_date_var)
        self.filter_date_entry.grid(row=0, column=3)

        filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=5)

        reset_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.load_data)
        reset_btn.grid(row=0, column=5, padx=5)

        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(3, weight=1)

    def add_training(self):
        date_str = self.date_entry.get()
        type_str = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Валидация даты
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return

        # Валидация длительности
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        # Добавление записи в таблицу
        self.tree.insert('', 'end', values=(date_str, type_str, duration_str))
        self.save_data()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def load_data(self):
        """Загружает данные из файла и отображает их"""
        self.tree.delete(*self.tree.get_children())
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                self.tree.insert('', 'end', values=(item['date'], item['type'], item['duration']))
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Ошибка при чтении файла данных.")

    def save_data(self):
        """Сохраняет текущие записи в JSON-файл"""
        data = []
        for row in self.tree.get_children():
            item = self.tree.item(row)['values']
            data.append({'date': item[0], 'type': item[1], 'duration': item[2]})
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def apply_filter(self):
        """Фильтрует записи по типу и дате"""
        filter_type = self.filter_type_var.get().lower().strip()
        filter_date = self.filter_date_var.get().strip()

        self.load_data()

        for row in self.tree.get_children():
            values = self.tree.item(row)['values']
            match_type = True
            match_date = True

            if filter_type:
                match_type = filter_type in str(values[1]).lower()
            if filter_date:
                match_date = (values[0] == filter_date)

            if not (match_type and match_date):
                self.tree.detach(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()