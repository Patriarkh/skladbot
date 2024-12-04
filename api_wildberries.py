import requests
import os
from dotenv import load_dotenv

load_dotenv()

WILDBERRIES_API_URL = "https://supplies-api.wildberries.ru/api/v1/warehouses"
HEADERS = {"Authorization": os.getenv("WILDBERRIES_API_TOKEN")}



def fetch_warehouses():
    response = requests.get(WILDBERRIES_API_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка API: {response.status_code}")
    

print(f"WILDBERRIES_API_TOKEN: {os.getenv('WILDBERRIES_API_TOKEN')}")

