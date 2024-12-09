import pandas as pd

# 1. Загрузка данных

def load_and_prepare_data(csv_file):
    # Читаем CSV файл
    data = pd.read_csv(csv_file)

    # Отделяем целевую переменую (Type) и признаки (импортированные DLL)
    # Получаем все столбцы, которые представляют собой DLL, кроме SHA256 и Type
    dll_columns = data.columns[2:]  # Все столбцы, начиная с третьего (индекс 2)
    X = data[dll_columns]
    y = data['Type']

    print(data['Type'].value_counts())

    return X, y


if __name__ == "__main__":
    dataset_file = './TestData/API_Functions.csv'
    X, y = load_and_prepare_data(dataset_file)
    # print("Признаки (X):")
    # print(X.head())
    # print("Целевая переменная (y):")
    # print(y.head())
    print(y.unique())
