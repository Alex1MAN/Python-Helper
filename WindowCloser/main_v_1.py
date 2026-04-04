import time
import threading
import tkinter as tk
import py_window_closer


def create_test_window(title):
    root = tk.Tk()
    root.title(title)
    root.geometry("300x100")
    label = tk.Label(root, text=f"Окно: {title}")
    label.pack(expand=True)

    # Обработчик закрытия окна через WM_CLOSE
    def on_close():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Ждём, пока окно закроется по сигналу
    root.mainloop()


def main():
    print("Запуск мониторинга окон...")
    py_window_closer.start_waiting()

    window_threads = []

    for i in range(3):
        print(f"\nИтерация {i + 1}: создание окна с заголовком 'текст1'")

        def run_window():
            create_test_window("текст1")

        window_thread = threading.Thread(target=run_window, daemon=True)
        window_thread.start()
        window_threads.append(window_thread)

        time.sleep(0.5)
        print("... мониторинг продолжает работать...")
        time.sleep(2)

    # Дожидаемся, пока все окна нормально закроются
    for th in window_threads:
        th.join(timeout=10)
    print("\nЗавершение мониторинга окон...")
    py_window_closer.stop_waiting()


if __name__ == "__main__":
    main()