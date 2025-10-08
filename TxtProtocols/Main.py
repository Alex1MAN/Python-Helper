from pathlib import Path
from datetime import datetime, timedelta
import time


def main():
    start_time = datetime.now()
    global prot_folder
    prot_folder = r'D:\PYTHON projects\TxtProtocols\Protocols'
    delete_old_detailed_logs()
    write_detailed_log("start", "Начало работы")
    time.sleep(2)
    write_detailed_log("work", "Середина работы")
    time.sleep(2)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    # Форматируем итоговое время в ЧЧ:ММ:СС
    total_time_str = str(elapsed_time).split('.')[0]
    write_detailed_log("end", f"Конец работы (затрачено времени {total_time_str} ЧЧ:ММ:СС)")


def delete_old_detailed_logs(days_old=14):
    folder = Path(prot_folder)
    cutoff_date = datetime.now() - timedelta(days=days_old)
    for file in folder.glob("*.txt"):
        if file.is_file():
            file_mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if file_mtime < cutoff_date:
                file.unlink()


def write_detailed_log(mode, text):
    folder = Path(prot_folder)
    today_str = datetime.now().strftime("%d.%m.%Y")
    filename = f"Детальный лог за {today_str}.txt"
    file_path = folder / filename
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    log_entry = f"{timestamp} | {text}"
    # Создаём файл, если не существует
    if not file_path.exists():
        file_path.touch()
    # Проверяем размер файла
    file_empty = file_path.stat().st_size == 0
    with file_path.open("a", encoding="utf-8") as f:
        if mode == "start":
            if not file_empty:
                f.write("\n\n")
            f.write(f"{log_entry}\n")
        if mode == "work":
            f.write(f"{log_entry}\n")
        if mode == "end":
            f.write(f"{log_entry}\n\n===============================")


try:
    main()
except Exception as e:
    print(f"Ошибка: {e}")
