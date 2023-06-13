import os
import csv
import time
import shutil


class DiskLoading:
    """
    Класс для измерения нагрузки на диск с помощью действий над файлами.
    """
    def __init__(self, file: str, attempts: int):
        self.file: str = file
        self.copy_file: str = f"{os.path.dirname(__file__)}/{os.path.basename(file)}"
        self.attempts: int = attempts

    def download_file(self) -> float:
        """
        Получение времени копирования файла.
        :return: Получаем время копирования файла.
        """
        start_time: time = time.time()
        shutil.copy(self.file, self.copy_file)
        end_time: time = time.time()
        return round(end_time - start_time, 4)

    def create_file(self) -> float:
        """
        Получение времени создания файла.
        :return: Получаем время создания файла.
        """
        chunk_size: int = 1024 * 1024  # 1 МБ
        with open(self.copy_file, 'wb') as file:
            data: bytes = b'\0' * chunk_size
            remaining_bytes: int = os.stat(self.file).st_size
            start_time: time = time.time()
            while remaining_bytes >= chunk_size:
                file.write(data)
                remaining_bytes -= chunk_size
            if remaining_bytes > 0:
                file.write(data[:remaining_bytes])
            end_time: time = time.time()
        return round(end_time - start_time, 4)

    def read_file(self) -> float:
        """
        Получение времени чтения файла.
        :return: Получаем время чтения файла.
        """
        start_time: time = time.time()
        with open(self.file, 'rb') as file:
            file.read()
        end_time: time = time.time()
        return round(end_time - start_time, 4)

    def save_test_results(self, results: list) -> None:
        """
        Сохранение результатов.
        :param results: Список с результатами замеров.
        :return:
        """
        with open(f"{os.path.dirname(self.copy_file)}/results.csv", 'w', newline='') as file:
            writer: csv.writer = csv.writer(file)
            writer.writerow(["Наименование файла", "Номер попытки", "Время скачивания", "Время чтения", "Время записи"])
            writer.writerows(results)

    def main(self) -> None:
        """
        Основная функция, которая запускает все действия, связанного с файлом.
        :return:
        """
        results: list = []
        for i in range(1, self.attempts + 1):
            download_time: float = self.download_file()
            write_time: float = self.create_file()
            read_time: float = self.read_file()
            results.append([os.path.basename(self.file), i, download_time, read_time, write_time])
        self.save_test_results(results)
        os.remove(self.copy_file)

disk_loading = DiskLoading(
    '/home/timur/sambashare/rzhd/rzhd_ktk/КТК 01-2022.xlsb',
    10
)
disk_loading.main()
