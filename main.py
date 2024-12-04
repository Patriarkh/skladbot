from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from db_setup import get_db_connection
from cache import cache_warehouse, get_from_cache
from api_wildberries import fetch_warehouses
import asyncio

# Загружаем переменные окружения
load_dotenv()

# Создаём экземпляры бота и диспетчера
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.reply("Привет! Напишите название склада, чтобы узнать его данные.")

# Обработчик сообщений с названием склада
@dp.message()
async def warehouse_handler(message: Message):
    warehouse_name = message.text

    # Проверка в Redis
    cached_data = get_from_cache(warehouse_name)
    if cached_data:
        await message.reply(f"Данные из кэша: {cached_data}")
        return

    # Проверка в PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM warehouses WHERE name = %s", (warehouse_name,))
    warehouse = cursor.fetchone()
    conn.close()

    if warehouse:
        data = f"ID: {warehouse[1]}, Коэффициент: {warehouse[3]}"
        cache_warehouse(warehouse_name, data)  # Кэшируем данные
        await message.reply(data)
    else:
        await message.reply("Склад не найден!")

# Функция обновления данных складов
async def update_warehouses():
    try:
        data = fetch_warehouses()  # Получение данных из API Wildberries
        conn = get_db_connection()
        cursor = conn.cursor()
        for warehouse in data:
            cursor.execute("""
                INSERT INTO warehouses (warehouse_id, name, coefficient)
                VALUES (%s, %s, %s)
                ON CONFLICT (warehouse_id) DO NOTHING;
            """, (warehouse['ID'], warehouse['name'], warehouse.get('coefficient', 1)))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка обновления данных складов: {e}")

# Основная функция
async def main():
    # Регистрируем обработчики
    dp.message.register(start_handler, Command("start"))
    dp.message.register(warehouse_handler)

    # Обновляем данные складов перед запуском бота
    await update_warehouses()

    # Запускаем бота
    await dp.start_polling(bot)

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
