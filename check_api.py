import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Укажите правильный URL для проверки API
WILDBERRIES_API_URL = "https://supplies-api.wildberries.ru/ping"

# Получаем токен из переменных окружения
HEADERS = {"Authorization": os.getenv("WILDBERRIES_API_TOKEN")}

def check_wb_connection():
    try:
        response = requests.get(WILDBERRIES_API_URL, headers=HEADERS)
        if response.status_code == 200:
            print("Подключение успешно: API работает!")
        elif response.status_code == 401:
            print("Ошибка 401: Токен недействителен или отсутствует.")
        elif response.status_code == 429:
            print("Ошибка 429: Превышен лимит запросов.")
        else:
            print(f"Ошибка подключения: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Проверяем подключение
check_wb_connection()
