import os
import csv
import time
import shutil
from typing import Union


class DiskLoading:
    """
    Класс для измерения нагрузки на диск с помощью действий над файлами.
    """
    def __init__(self, file: str, attempts: int):
        self.file: str = file
        self.copy_file: str = f"{os.getcwd()}/{os.path.basename(file)}"
        self.attempts: int = attempts

    def get_size(self, unit: str = 'bytes') -> Union[float, int]:
        """
        Получение размера файла.
        :return: Получаем размер файла.
        """
        file_size: int = os.path.getsize(self.file)
        exponents_map: dict = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
        if unit not in exponents_map:
            raise ValueError("Must select from ['bytes', 'kb', 'mb', 'gb']")
        size: float = file_size / 1024 ** exponents_map[unit]
        return int(size) if unit == 'bytes' else round(size, 3)

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
            remaining_bytes: int = self.get_size()
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
        file_path = os.path.join(os.path.dirname(self.copy_file), "results.csv")
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if os.stat(file_path).st_size == 0:
                writer.writerow(
                    ["Наименование файла", "Размер файла", "Номер попытки", "Время скачивания", "Время чтения",
                     "Время записи"]
                )
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
            results.append([os.path.basename(self.file), self.get_size('mb'), i, download_time, read_time, write_time])
        self.save_test_results(results)
        os.remove(self.copy_file)

disk_loading = DiskLoading(
    '/home/timur/sambashare/rzhd/rzhd_ktk/КТК 01-2022.xlsb',
    1
)
disk_loading.main()
