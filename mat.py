import inspect

# Хак для совместимости версий inspect (если нужно)
if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec

import tkinter as tk
from tkinter import messagebox
from pyfirmata import Arduino, PWM

# --- Логика работы с Arduino ---
# (Оставляем без изменений, но добавьте проверку COM-порта перед запуском)
try:
    board = Arduino("COM6")
    board.digital[3].mode = PWM
    board.digital[5].mode = PWM
except Exception as e:
    messagebox.showerror("Ошибка подключения", f"Не удалось подключить Arduino:\n{e}")
    # Для теста интерфейса без Arduino можно закомментировать exit() ниже
    #exit()

# --- Функции логики ---
def change_brightness(val):
    try:
        brightness = float(val) / 100.0
        board.digital[3].write(brightness)
    except Exception:
        pass

def LedON(event=None):
    LEDbright.set(100)

def LedOFF(event=None):
    LEDbright.set(0)

def aboutMsg():
    messagebox.showinfo("О программе", "Dimmer Control v2.1\n\nУправление яркостью LED через Arduino.\nИсправлен диммер.")

def closeApp():
    if messagebox.askokcancel("Выход", "Закрыть приложение?"):
        win.destroy()

# --- Создание графического интерфейса ---
win = tk.Tk()
win.title("Arduino LED Dimmer")
win.geometry("320x400") # Немного увеличили высоту для новых кнопок
win.resizable(False, False)

# Основной контейнер с отступами
main_frame = tk.Frame(win, padx=10, pady=10)
main_frame.pack(fill="both", expand=True)

# === БЛОК 1: Настройки ===
settings_frame = tk.LabelFrame(main_frame, text="Настройки")
settings_frame.pack(fill="x", pady=5)

tk.Label(settings_frame, text="Задержка (сек):").pack(side="left", padx=10, pady=10)
LEDtime = tk.Entry(settings_frame, width=10, justify="center")
LEDtime.insert(0, "0.5")
LEDtime.pack(side="left", padx=10, pady=10)

# === БЛОК 2: Управление Светом ===
control_frame = tk.LabelFrame(main_frame, text="Управление Яркостью")
control_frame.pack(fill="x", pady=5)

# Шкала
LEDbright = tk.Scale(control_frame, 
                     from_=0, 
                     to=100, 
                     orient=tk.HORIZONTAL, 
                     length=250,
                     label="Уровень мощности (%)", 
                     tickinterval=25,
                     command=change_brightness)
LEDbright.set(50)
LEDbright.pack(pady=10)

# Фрейм для кнопок ВКЛ/ВЫКЛ внутри блока управления
btn_frame = tk.Frame(control_frame)
btn_frame.pack(fill="x", pady=5)

# Кнопки управления (растягиваем их поровну)
bluebtn = tk.Button(btn_frame, text="ВКЛ (1)", command=LedON, bg="#ddddff", height=2)
bluebtn.pack(side="left", fill="x", expand=True, padx=5)

redbtn = tk.Button(btn_frame, text="ВЫКЛ (0)", command=LedOFF, bg="#ffdddd", height=2)
redbtn.pack(side="right", fill="x", expand=True, padx=5)

# === БЛОК 3: Системные кнопки (Info, Exit) ===
system_frame = tk.Frame(main_frame)
system_frame.pack(fill="x", pady=15, side="bottom")

info_btn = tk.Button(system_frame, text="Info", command=aboutMsg, width=10)
info_btn.pack(side="left", padx=5)

exit_btn = tk.Button(system_frame, text="Exit", command=closeApp, width=10, bg="#f0f0f0")
exit_btn.pack(side="right", padx=5)

# --- Привязка горячих клавиш ---
win.bind('<KeyPress-1>', LedON)
win.bind('<KeyPress-0>', LedOFF)
win.bind('<Control-q>', lambda e: closeApp())

win.mainloop()