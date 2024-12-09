import os
import pefile
import joblib
import pandas as pd
import datetime
# 1. Извлечение признаков файла
def extract_features_from_files(file_path, libraries):
     """
    Извлекает признаки из PE-файла (наличие определенных библиотек).
    :param file_path: Путь к файлу
    :param libraries: Список библиотек для проверки
    :return: Список 0 и 1, где 1 означает, что библиотека импортируется
    """
     try:
          pe = pefile.PE(file_path)
          imported_libs = [entry.dll.decode('utf-8').lower() for entry in pe.DIRECTORY_ENTRY_IMPORT]
          return [1 if lib in imported_libs else 0 for lib in libraries]
     except Exception as e:
          print(f"Ошибка анализа файла {file_path}: {e}")
          return None

# 2. Сканирование папки
def scan_folder(folder_path, model, libraries):
    """
    Сканирует папку и классифицирует файлы на вирусы и безопасные.
    :param folder_path: Путь к папке для сканирования
    :param model: Загруженная обученная модель
    :param libraries: Список библиотек для анализа
    :return: Список результатов
    """
    malware_types = {
    0: "Доброкачественный",  # Benign
    1: "RedLineStealer",      # RedLineStealer (можно оставить без перевода, так как это название)
    2: "Загрузчик",          # Downloader
    3: "RAT",                # RAT (можно оставить без перевода, так как это аббревиатура)
    4: "Банковский троян",   # BankingTrojan
    5: "Клавиатурный шпион",  # SnakeKeyLogger
    6: "Шпионское ПО"        # Spyware
}
    result = []

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith('.exe'):
                features = extract_features_from_files(file_path, libraries)
                if features:
                    prediction = model.predict([features])[0]
                    if prediction in malware_types:
                        result.append((file_path, f"Тип {prediction} ({malware_types[prediction]})"))
                    else:
                        result.append((file_path, "Неизвестный тип"))

    return result

# 3. Сохранение отчета
def save_results_to_csv(results, output_path):
    """
    Сохраняет результаты сканирования в CSV-файл.
    :param results: Список результатов [(путь к файлу, результат)]
    :param output_path: Путь к CSV-файлу
    """
    df = pd.DataFrame(results, columns=["Файл", "Результат"])
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Результаты сохранены в файл: {output_path}")

# Основная часть программы
if __name__ == "__main__":
    # Путь к модели и папке для сканирования
    model_path = "virus_detection_model.pkl"
    folder_to_scan = "C:/Users/daniyal/Desktop"
    output_csv = f"scan_results-{datetime.date.today()}.csv"

    data = pd.read_csv('./TestData/API_Functions.csv')
    libraries = data.columns[2:]

    # Загружаем модель
    model = joblib.load(model_path)

    # Сканируем папку
    results = scan_folder(folder_to_scan, model, libraries)

    # Сохраняем результаты
    save_results_to_csv(results, output_csv)
