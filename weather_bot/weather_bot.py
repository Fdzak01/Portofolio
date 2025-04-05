import os
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.filters import Command

import asyncio

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY_WEATHER = os.getenv("API_KEY_WEATHER")

# Create bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Handle /start
@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Halo! Kirim /cuaca [nama_kota] untuk melihat info cuaca.")

# Handle /cuaca
@router.message(Command("cuaca"))
async def cuaca_cmd(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Gunakan format: /cuaca [nama_kota]")
        return

    city = args[1]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}&units=metric"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        suhu = data["main"]["temp"]
        deskripsi = data["weather"][0]["description"]
        kelembaban = data["main"]["humidity"]

        reply = (
            f"📍 Cuaca di *{city.title()}*:\n"
            f"🌡 Suhu: {suhu}°C\n"
            f"☁️ Deskripsi: {deskripsi}\n"
            f"💧 Kelembaban: {kelembaban}%"
        )
        await message.answer(reply, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("❌ Kota tidak ditemukan!")

# Start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
