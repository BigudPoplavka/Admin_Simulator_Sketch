import sys, os
import tkinter as tk
from tkinter import ttk
from tkinter import Radiobutton, StringVar, Text
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

sys.path.append('net_management_part')

from net_management_part.net_management import *
from net_management_part.console_emulator import *
from AI_agents.QA_model import QA_Model_ML
from AI_agents.dataset.dataset_parser import DatasetParser


path = os.path.join(os.getcwd(), "AI_agents\\dataset") 
parser = DatasetParser(path)
dataset = parser.parse_all_dataset()
qa_model_ml = QA_Model_ML(dataset)


def get_sreen_size(window):
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    
    return [width, height]

def show_frame(frame):
    frame.tkraise()

# МЕНЮ 

def create_new_file():
    return

def save_file():
    return

# ЛЕВАЯ ПАНЕЛЬ МЕНЮ (разделы тренажера)

def open_net_manage_window(frame):
    show_frame(frame)

def open_sys_monitoring(frame):
    show_frame(frame)

def open_automatization_window(frame):
    show_frame(frame)

def main():
    root = tk.Tk()
    root.title("Обучающий тренажер системного администратора")
    screen_size = get_sreen_size(root)
    root.geometry(f"{screen_size[0]}x{screen_size[1]}")  
    
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Новый", command=create_new_file)
    file_menu.add_command(label="Сохранить", 
                        command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Закрыть", command=lambda: root.quit())
    menu_bar.add_cascade(label="Файл", menu=file_menu)
    menu_bar.add_cascade(label="О программе")
    root.config(menu=menu_bar)

# ГЛАВНЫЙ КОНТЕЙНЕР (контейнер блоков)

    parent_frame = tk.Frame(root)
    parent_frame.pack(fill="both", expand=True)

# ЛЕВОСТОРОННЕЕ МЕНЮ КАТЕГОРИЙ

    menu_frame = tk.Frame(parent_frame, bg="gray", width=200)
    menu_frame.pack(side="left", fill="y")

    button1 = tk.Button(menu_frame, 
                        text="Управлене сетью", 
                        command=lambda: show_frame(net_manage_window))
    button1.pack(pady=1, fill="x")

    button2 = tk.Button(menu_frame, 
                        text="Мониторинг системы", 
                        command=lambda: show_frame(sys_monitoring_window))
    button2.pack(pady=1, fill="x")

# КОНТЕЙНЕР ТЕМАТИЧЕСКИХ БЛОКОВ (главного контента)

    frames_block = ttk.Frame(parent_frame)
    frames_block.pack(side="left", fill="both", expand=True)

# УПРАВЛЕНИЕ СЕТЬЮ
# Фрейм и вкладки раздела  

    net_manage_window = ttk.Frame(frames_block)

    net_manage_notebook = ttk.Notebook(net_manage_window, width=850, height=750)
    net_manage_notebook.pack(fill="both", expand=True)
    
    nm_tab1 = ttk.Frame(net_manage_notebook)
    net_manage_notebook.add(nm_tab1, text="Моделирование сетевой инфраструктуры")
    
    nm_tab1_content = get_net_management_window(nm_tab1)
    nm_tab1_content.pack(fill="both", side="left")

    nm_tab2 = ttk.Frame(net_manage_notebook)
    net_manage_notebook.add(nm_tab2, text="Настройка VLAN")
    nm_label2 = tk.Label(nm_tab2, text=task_vlan.description)
    nm_label2.pack(padx=10, pady=10)

    emulator = get_emulator_window(nm_tab2)
    emulator.set_task(task_vlan)
    emulator.pack()

# МОНИТОРИНГ СИСТЕМЫ
# Фрейм и вкладки раздела

    sys_monitoring_window = ttk.Frame(frames_block)

    sys_monitoring_notebook = ttk.Notebook(sys_monitoring_window, width=500)
    sys_monitoring_notebook.pack(fill="both", expand=True)
    
    sm_tab1 = ttk.Frame(sys_monitoring_notebook)
    sys_monitoring_notebook.add(sm_tab1, text="Вкладка 2.1")
    sm_label1 = tk.Label(sm_tab1, text="Содержимое вкладки 2.1")
    sm_label1.pack(padx=10, pady=10)

# РАЗМЕЩЕНИЕ И ОТОБРАЖЕНИЕ ФРЕЙМОВ

    net_manage_window.grid(row=0, column=0, sticky="nsw")
    sys_monitoring_window.grid(row=0, column=0, sticky="nsw")

    sm_content_label = tk.Label(sys_monitoring_window, text="Фрейм 2")
    sm_content_label.pack(padx=20, pady=20)

# БЛОК ИНТЕЛЛЕКТУАЛЬНОГО ПОМОЩНИКА

    def submit_text():
        user_input = text_input.get(1.0, tk.END)
        text_input.config(state=tk.NORMAL)
        text_input.delete(1.0, tk.END)

        if not user_input.strip():
            messagebox.showwarning("Упс!", "Пустой ввод!")
            return
        try:
            result = qa_model_ml.get_answer(user_input)[0][2:]
            text_input.insert(tk.END, f"\nОТВЕТ: {result}")
        except Exception as e:
            messagebox.showwarning("Упс!", f"Текст ошибки: {e}")


    text_input = tk.Text(parent_frame, wrap="word", background="#606060", foreground="#ffffff")
    text_input.pack(pady=20)

    answer_text = tk.Label(parent_frame)
    answer_text.pack(side="left")

    submit_button = tk.Button(parent_frame, 
                              text="Отправить", width=40,
                              command=submit_text)
    submit_button.pack(side="left")

    net_manage_window.tkraise()
    root.mainloop()


if __name__ == "__main__":

    test_questions = [
        "Что такое VLAN?",
        "Как настроить DHCP на маршрутизаторе для автоматической выдачи IP-адресов клиентам в сети?",
        "Конфликт IP-адресов в сети",
        "Отказ в работе VPN из-за несовместимости параметров настройки",
        "Что такое дуплекс",
        "Что делает команда show version?",
        "show interfaces switchport?"
    ]

    for question in test_questions:
        answer = qa_model_ml.get_answer(question)[0][2:]
        print(f"Вопрос: {question}")
        print(f"Ответ: {answer}\n")

    main()
