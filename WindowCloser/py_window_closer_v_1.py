import ctypes
import threading
import time
import win32gui  # pip install pywin32
import win32con

# Определяем некоторые WinAPI‑функции вручную, если нужно
user32 = ctypes.windll.user32

# Константа для отправки сообщения WM_CLOSE
WM_CLOSE = win32con.WM_CLOSE


class WindowCloser:
    def __init__(self):
        # Работаем с заголовками, которые нужно отслеживать
        self.target_titles = ["текст1", ["текст2"]]  # можно добавить другие
        self._running = False
        self._thread = None

    def _find_and_close_target_windows(self):
        """
        Основной цикл: каждые несколько секунд проверяет,
        есть ли окно с нужным заголовком и закрывает его.
        """
        while self._running:
            try:
                # Перечисляем все окна
                def enum_window(hwnd, _):
                    # Получаем текст заголовка окна
                    length = win32gui.GetWindowTextLength(hwnd)
                    if length == 0:
                        return True

                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text in self.target_titles:
                        # Пытаемся отправить WM_CLOSE
                        win32gui.SendMessage(hwnd, WM_CLOSE, 0, 0)
                win32gui.EnumWindows(enum_window, None)
            except Exception:
                pass  # Игнорируем ошибки при перечислении окон

            # Задержка между проверками (например, 1 c)
            time.sleep(1)

    def start_waiting(self):
        """
        Запускает фоновый поток для ожидания и закрытия окон.
        Если уже запущен - не делаем ничего.
        """
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._find_and_close_target_windows,
            daemon=True,
        )
        self._thread.start()

    def stop_waiting(self):
        """
        Останавливает ожидание: завершает цикл в потоке.
        """
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2)  # ждём завершения потока


# Экземпляр по умолчанию для удобства
_window_closer = WindowCloser()


def start_waiting():
    """
    Запускает фоновый поток, который будет искать
    и закрывать окна с заголовками из target_titles.
    """
    _window_closer.start_waiting()


def stop_waiting():
    """
    Останавливает фоновый поток поиска и закрытия окон.
    """
    _window_closer.stop_waiting()