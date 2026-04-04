# main.py

import time
import threading
import tkinter as tk
import win32gui
import py_window_closer


target_title = "текст1"

# Глобальные события
window_closed_event = threading.Event()   # True, когда окно закрыто
window_seen = threading.Event()           # True, когда окно уже появлялось


def find_window_handle_by_title(title):
    """
    Ищет окно по заголовку и возвращает его hwnd.
    Если не найдено — None.
    """
    result = None

    def enum_window(hwnd, _):
        nonlocal result
        length = win32gui.GetWindowTextLength(hwnd)
        if length == 0:
            return True
        window_text = win32gui.GetWindowText(hwnd)
        if window_text == title:
            result = hwnd
            return False
        return True

    win32gui.EnumWindows(enum_window, None)
    return result


def is_window_exists(hwnd):
    """
    Проверяет, существует ли окно по hwnd.
    """
    return bool(hwnd and win32gui.IsWindow(hwnd))


def monitor_window():
    """
    Фоновый поток: не блокирует main.py, периодически проверяет окно.
    """
    hwnd = None

    while True:
        # Проверка появления окна
        if not window_seen.is_set():
            hwnd = find_window_handle_by_title(target_title)
            if hwnd is not None:
                print("[monitor] Окно появилось, ожидаем его закрытия...")
                window_seen.set()
                window_closed_event.clear()

        # Проверка закрытия
        if window_seen.is_set() and hwnd is not None:
            if not is_window_exists(hwnd):
                print("[monitor] Окно закрыто! Основной скрипт может продолжить.")
                window_closed_event.set()
                hwnd = None
                window_seen.clear()

        time.sleep(0.3)  # не слишком часто


def create_all_tk_windows():
    """
    Единый Tk‑цикл в одном потоке.
    Создаёт несколько окон 'текст1' по очереди.
    """
    # 1 окно
    print("[tk_thread] Создаём первое окно 'текст1'...")
    root1 = tk.Tk()
    root1.title(target_title)
    root1.geometry("320x120")
    tk.Label(root1, text="Окно 1: текст1").pack(expand=True)

    def on_close1():
        root1.quit()
        root1.destroy()

    root1.protocol("WM_DELETE_WINDOW", on_close1)
    root1.mainloop()

    time.sleep(0.5)

    # 2 окно
    print("[tk_thread] Создаём второе окно 'текст1'...")
    root2 = tk.Tk()
    root2.title(target_title)
    root2.geometry("320x120")
    tk.Label(root2, text="Окно 2: текст1").pack(expand=True)

    def on_close2():
        root2.quit()
        root2.destroy()

    root2.protocol("WM_DELETE_WINDOW", on_close2)
    root2.mainloop()

    time.sleep(0.5)

    # 3 окно
    print("[tk_thread] Создаём третье окно 'текст1'...")
    root3 = tk.Tk()
    root3.title(target_title)
    root3.geometry("320x120")
    tk.Label(root3, text="Окно 3: текст1").pack(expand=True)

    def on_close3():
        root3.quit()
        root3.destroy()

    root3.protocol("WM_DELETE_WINDOW", on_close3)
    root3.mainloop()


def main():
    print("Запуск основного скрипта...")

    # Запускаем мониторинг окон в отдельном потоке
    monitor_thread = threading.Thread(target=monitor_window, daemon=True)
    monitor_thread.start()

    # Запускаем демон‑модуль закрытия окон
    py_window_closer.start_waiting()

    # ————— ПРИМЕР 1: выполнение основного кода —————
    print("\n[main] ПРИМЕР 1: обычный код (никаких Tk в main thread)...")
    for i in range(3):
        print(f"main.py: шаг {i + 1}")
        time.sleep(0.5)

    # ————— ПРИМЕР 2: запускаем окна в отдельном потоке с ЕДИНСТВЕННЫМ mainloop() —————
    print("\n[main] ПРИМЕР 2: создание всех окон с заголовком 'текст1' в одном потоке...")
    tk_thread = threading.Thread(target=create_all_tk_windows, daemon=True)
    tk_thread.start()
    # даём окну жить, но не блокируем mainloop — он живёт в tk_thread
    time.sleep(0.5)

    # ————— ОЖИДАНИЕ ЗАКРЫТИЯ ОКНА(ЕН) —————
    if window_seen.is_set():
        print("main.py: окно возникло, ожидаем его закрытия...")
        window_closed_event.wait(timeout=20)  # максимум 20 секунд
        print("main.py: окно закрыто, продолжаем выполнение.")
    else:
        print("main.py: окна с 'текст1' не было или оно уже закрыто.")

    # ————— ПРИМЕР 3: продолжение кода —————
    print("main.py: продолжаем выполнение после закрытия окна...")
    for i in range(5):
        print(f"main.py: продолжение шаг {i + 1}")
        time.sleep(0.5)

    # Остановка демонов
    py_window_closer.stop_waiting()
    print("main.py: работа завершена.")


if __name__ == "__main__":
    main()