# py_window_closer.py

import threading
import time
import win32gui
import win32con

# Определяем WM_CLOSE
WM_CLOSE = win32con.WM_CLOSE


class WindowCloser:
    def __init__(self):
        self.target_titles = ["текст1"]  # можно добавить другие
        self._running = False
        self._thread = None

    def _find_and_close_target_windows(self):
        while self._running:
            try:
                def enum_window(hwnd, _):
                    length = win32gui.GetWindowTextLength(hwnd)
                    if length == 0:
                        return True
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text in self.target_titles:
                        print(f"[py_window_closer] Закрываю окно: '{window_text}'")
                        win32gui.SendMessage(hwnd, WM_CLOSE, 0, 0)
                    return True

                win32gui.EnumWindows(enum_window, None)
            except Exception as e:
                print(f"[py_window_closer] Ошибка при перечислении окон: {e}")

            time.sleep(0.3)  # не слишком часто

    def start_waiting(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._find_and_close_target_windows,
            daemon=True,
        )
        self._thread.start()

    def stop_waiting(self):
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2)


# Глобальный экземпляр для удобства
_window_closer = WindowCloser()


def start_waiting():
    """Запуск фонового монитора окон и их закрытия по заголовку."""
    _window_closer.start_waiting()


def stop_waiting():
    """Остановка фонового монитора окон."""
    _window_closer.stop_waiting()