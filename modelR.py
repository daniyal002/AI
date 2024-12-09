from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from loadData import load_and_prepare_data
import pandas as pd

# 1. Обучение модели
def train_model(X, y, model_output):
    # Разделяем данные на тренировочную и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

    # Создаем модель Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train,y_train)

    # Оцениваем модель
    y_pred = model.predict(X_test)
    print("Отчет о классификации:")
    print(classification_report(y_test,y_pred))

    # Сохраняем модель в файл
    joblib.dump(model, model_output)
    print(f"Модель сохранена: {model_output}")

# Проверка
if __name__ == "__main__":
    # Загрузка данных из API_Functions.csv
    api_file = './TestData/API_Functions.csv'
    X_api, y_api = load_and_prepare_data(api_file)

# Проверка размеров
    print("Размеры наборов данных:")
    print("X_api:", X_api.shape, "y_api:", y_api.shape)


    model_output = "virus_detection_model.pkl"
    train_model(X_api, y_api, model_output)
