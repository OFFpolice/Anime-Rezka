import os
import logging
from dotenv import load_dotenv
from os.path import join, dirname
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.exceptions import MessageNotModified
from rezka_scraper import RezkaScraper

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
scraper = RezkaScraper()

async def send_anime_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    matches = await scraper.search_anime(page)
    if matches:
        response = "<b>🍿 Найденные аниме:</b>\n"
        for title, link in matches:
            response += f"🔹 <a href=\"{link}\">{title}</a>\n"
        response += f"\n<b>🤖: @{bot_username} | 📑: {page}</b>"
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if page > 1:
            keyboard.insert(types.InlineKeyboardButton("« Назад", callback_data=f"anime_page:{page-1}"))
        keyboard.insert(types.InlineKeyboardButton("Вперёд »", callback_data=f"anime_page:{page+1}"))
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

async def send_movies_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    matches = await scraper.search_movies(page)
    if matches:
        response = "<b>🍿 Найденные фильмы:</b>\n"
        for title, link in matches:
            response += f"🔹 <a href=\"{link}\">{title}</a>\n"
        response += f"\n<b>🤖: @{bot_username} | 📑: {page}</b>"
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if page > 1:
            keyboard.insert(types.InlineKeyboardButton("« Назад", callback_data=f"movie_page:{page-1}"))
        keyboard.insert(types.InlineKeyboardButton("Вперёд »", callback_data=f"movie_page:{page+1}"))
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

async def send_series_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    matches = await scraper.search_series(page)
    if matches:
        response = "<b>📺 Найденные сериалы:</b>\n"
        for title, link in matches:
            response += f"🔹 <a href=\"{link}\">{title}</a>\n"
        response += f"\n<b>🤖: @{bot_username} | 📑: {page}</b>"
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if page > 1:
            keyboard.insert(types.InlineKeyboardButton("« Назад", callback_data=f"series_page:{page-1}"))
        keyboard.insert(types.InlineKeyboardButton("Вперёд »", callback_data=f"series_page:{page+1}"))
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

async def send_cartoon_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    matches = await scraper.search_cartoons(page)
    if matches:
        response = "<b>🍿 Найденные мультфильмы:</b>\n"
        for title, link in matches:
            response += f"🔹 <a href=\"{link}\">{title}</a>\n"
        response += f"\n<b>🤖: @{bot_username} | 📑: {page}</b>"
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        if page > 1:
            keyboard.insert(types.InlineKeyboardButton("« Назад", callback_data=f"cartoon_page:{page-1}"))
        keyboard.insert(types.InlineKeyboardButton("Вперёд »", callback_data=f"cartoon_page:{page+1}"))
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
        "✨ Добро пожаловать! Я твой виртуальный гид в мире аниме, фильмов, сериалов и мультфильмов. 🌌\n\n"
        "🔍 Хочешь найти что-то интересное для просмотра на вечер?\n"
        "Просто напиши название аниме, фильма, сериала или мультфильма, "
        "и я помогу тебе отыскать это на платформе Rezka.ag.\n\n"
        "📺 Готов окунуться в приключения?\n"
        "Нажимай на кнопки ниже или отправь название, чтобы начать поиск!"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🎬 Аниме", callback_data="search_anime"),
        types.InlineKeyboardButton("🎬 Фильмы", callback_data="search_movies"),
        types.InlineKeyboardButton("🎬 Сериалы", callback_data="search_series"),
        types.InlineKeyboardButton("🎬 Мультфильмы", callback_data="search_cartoons")
    )
    keyboard.add(types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"))
    await bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, protect_content=True)

@dp.callback_query_handler(lambda c: c.data.startswith(("search_anime", "search_movies", "search_series", "search_cartoons")))
async def start_search(callback_query: types.CallbackQuery):
    search_texts = {
        "search_anime": "Поиск аниме... ⏳⌛️⏳",
        "search_movies": "Поиск фильмов... ⏳⌛️⏳",
        "search_series": "Поиск сериалов... ⏳⌛️⏳",
        "search_cartoons": "Поиск мультфильмов... ⏳⌛️⏳"
    }
    search_functions = {
        "search_anime": send_anime_list,
        "search_movies": send_movies_list,
        "search_series": send_series_list,
        "search_cartoons": send_cartoon_list
    }
    await callback_query.answer(search_texts[callback_query.data], show_alert=True)
    await search_functions[callback_query.data](callback_query.message.chat.id, callback_query.message.message_id, page=1)

@dp.callback_query_handler(lambda c: c.data.startswith(("anime_page:", "movie_page:", "series_page:", "cartoon_page:")))
async def process_page_callback(callback_query: types.CallbackQuery):
    search_texts = {
        "anime_page": "Загружаем страницу аниме... ⏳⌛️⏳",
        "movie_page": "Загружаем страницу фильмов... ⏳⌛️⏳",
        "series_page": "Загружаем страницу сериалов... ⏳⌛️⏳",
        "cartoon_page": "Загружаем страницу мультфильмов... ⏳⌛️⏳"
    }
    search_functions = {
        "anime_page": send_anime_list,
        "movie_page": send_movies_list,
        "series_page": send_series_list,
        "cartoon_page": send_cartoon_list
    }
    content_type, page = callback_query.data.split(":")
    page = int(page)
    alert_text = search_texts[content_type]
    handler_function = search_functions[content_type]
    await callback_query.answer(alert_text, show_alert=False)
    await handler_function(callback_query.message.chat.id, callback_query.message.message_id, page)

@dp.callback_query_handler(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback_query: types.CallbackQuery):
    welcome_text = (
        "✨ Добро пожаловать! Я твой виртуальный гид в мире аниме, фильмов, сериалов и мультфильмов. 🌌\n\n"
        "🔍 Хочешь найти что-то интересное для просмотра на вечер?\n"
        "Просто напиши название аниме, фильма, сериала или мультфильма, "
        "и я помогу тебе отыскать это на платформе Rezka.ag.\n\n"
        "📺 Готов окунуться в приключения?\n"
        "Нажимай на кнопки ниже или отправь название, чтобы начать поиск!"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🎬 Аниме", callback_data="search_anime"),
        types.InlineKeyboardButton("🎬 Фильмы", callback_data="search_movies"),
        types.InlineKeyboardButton("🎬 Сериалы", callback_data="search_series"),
        types.InlineKeyboardButton("🎬 Мультфильмы", callback_data="search_cartoons")
    )
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
    title, link = await scraper.search_rezka(name)
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
