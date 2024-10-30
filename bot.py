import os
import aiohttp
import logging
from dotenv import load_dotenv
from os.path import join, dirname
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import MessageNotModified
from bs4 import BeautifulSoup


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


API_TOKEN = os.environ.get("API_TOKEN")


if not API_TOKEN:
    raise ValueError("API_TOKEN не найден. Убедитесь, что он указан в .env файле.")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="a",
    filename="bot.log"
)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def search_rezka(name):
    search_name = "https://rezka.ag/search/?do=search&subaction=search&q"
    params = {"q": name}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(search_name, params=params, headers=headers) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                results = soup.find_all("div", class_="b-content__inline_item")
                for result in results:
                    title = result.find("div", class_="b-content__inline_item-link").find("a").text
                    link = result.find("div", class_="b-content__inline_item-link").find("a")["href"]
                    if name.lower() in title.lower():
                        return title, link
    return None, None


async def search_anime(page=1):
    url = f"https://rezka.ag/animation/page/{page}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    results = soup.find_all("div", class_="b-content__inline_item")
                    matches = []
                    for result in results:
                        title = result.find("div", class_="b-content__inline_item-link").find("a").text.strip()
                        link = result.find("a")["href"]
                        matches.append((title, link))
                    return matches
                else:
                    return None
    except aiohttp.ClientError:
        return None


async def send_anime_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    matches = await search_anime(page)
    if matches:
        response = "<b>🍿 Найденные аниме:</b>\n"
        for title, link in matches:
            response += f"🔹 <a href=\"{link}\">{title}</a>\n"
        response += f"\n<b>🤖: @{bot_username} | 📑: {page}</b>"
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if page > 1:
            keyboard.insert(types.InlineKeyboardButton("« Назад", callback_data=f"page:{page-1}"))
        keyboard.insert(types.InlineKeyboardButton("Вперёд »", callback_data=f"page:{page+1}"))
        keyboard.insert(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        keyboard.add(
            types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"),
            types.InlineKeyboardButton("🐹 $HMSTR", url="https://t.me/hamster_kombat_boT/start?startapp=kentId1741564693")
        )
        try:
            await bot.edit_message_text(
                response, chat_id, message_id,
                parse_mode=types.ParseMode.HTML,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        except MessageNotModified:
            pass
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        try:
            await bot.edit_message_text(
                "<b>❌ Ничего не найдено!</b>", chat_id, message_id, 
                parse_mode=types.ParseMode.HTML,
                reply_markup=keyboard
            )
        except MessageNotModified:
            pass


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    welcome_text = (
        "👋 Привет, искатель аниме!\n\n"
        "Я помогу тебе найти самые интересные аниме с платформы Rezka.ag.\n"
        "Ты сможешь выбрать и перейти к просмотру любимых аниме!\n\n"
        "🎬 Нажми на кнопку ниже, чтобы начать поиск, и следи за процессом загрузки — скоро ты увидишь результаты! 🚀"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton("🎬 Искать аниме", callback_data="search_anime"))
    keyboard.add(types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"))
    await bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, protect_content=True)


@dp.callback_query_handler(lambda c: c.data == 'search_anime')
async def start_search(callback_query: types.CallbackQuery):
    await callback_query.answer("Начинаем поиск аниме... ⏳⌛️⏳", show_alert=True)
    await send_anime_list(callback_query.message.chat.id, callback_query.message.message_id, page=1)


@dp.callback_query_handler(lambda c: c.data.startswith('page:'))
async def process_page_callback(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split(":")[1])
    await callback_query.answer("Загружаем страницу... ⏳⌛️⏳")
    await send_anime_list(callback_query.message.chat.id, callback_query.message.message_id, page)


@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def back_to_main_menu(callback_query: types.CallbackQuery):
    welcome_text = (
        "👋 Привет, искатель аниме!\n\n"
        "Я помогу тебе найти самые интересные аниме с платформы Rezka.ag.\n"
        "Ты сможешь выбрать и перейти к просмотру любимых аниме!\n\n"
        "🎬 Нажми на кнопку ниже, чтобы начать поиск, и следи за процессом загрузки — скоро ты увидишь результаты! 🚀"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton("🎬 Искать аниме", callback_data="search_anime"))
    keyboard.add(types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"))
    await callback_query.answer("Возвращаемся в главное меню...", show_alert=True)
    try:
        await bot.edit_message_text(welcome_text, callback_query.message.chat.id, callback_query.message.message_id, reply_markup=keyboard)
    except MessageNotModified:
        pass


@dp.message_handler(content_types="text")
async def send_link(message: types.Message):
    name = message.text
    await bot.send_chat_action(message.chat.id, "typing")
    title, link = await search_rezka(name)
    if title:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("🍿 Смотреть на Rezka.ag", url=f"{link}"))
        keyboard.add(types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"))
        await message.answer(f"<b>🔍 Вот что мне удалось найти:</b>\n<a href=\"{link}\">{title}</a>", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    else:
        await message.answer("❌ Извините, но я не смог найти это на Rezka.ag.")
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
