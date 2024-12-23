import os
import logging
import hashlib
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

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
scraper = RezkaScraper()

async def send_anime_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    try:
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
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
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
                    "<b>❌ Ничего не найдено!</b>",
                    chat_id,
                    message_id,
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=keyboard
                )
            except MessageNotModified:
                pass
    except Exception as e:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        error_message = f"<b>⚠️ Произошла ошибка при обработке запроса. Попробуйте снова позже.</b>\n\n<b>❌ Ошибка:</b> <code>{e}</code>"
        try:
            await bot.edit_message_text(
                error_message,
                chat_id,
                message_id,
                parse_mode=types.ParseMode.HTML,
                reply_markup=keyboard
            )
        except MessageNotModified:
            pass

async def send_movies_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    try:
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
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
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
                    "<b>❌ Ничего не найдено!</b>",
                    chat_id,
                    message_id,
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=keyboard
                )
            except MessageNotModified:
                pass
    except Exception as e:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        error_message = f"<b>⚠️ Произошла ошибка при обработке запроса. Попробуйте снова позже.</b>\n\n<b>❌ Ошибка:</b> <code>{e}</code>"
        try:
            await bot.edit_message_text(
                error_message,
                chat_id,
                message_id,
                parse_mode=types.ParseMode.HTML,
                reply_markup=keyboard
            )
        except MessageNotModified:
            pass

async def send_series_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    try:
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
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
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
                    "<b>❌ Ничего не найдено!</b>",
                    chat_id,
                    message_id,
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=keyboard
                )
            except MessageNotModified:
                pass
    except Exception as e:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        error_message = f"<b>⚠️ Произошла ошибка при обработке запроса. Попробуйте снова позже.</b>\n\n<b>❌ Ошибка:</b> <code>{e}</code>"
        try:
            await bot.edit_message_text(
                error_message,
                chat_id,
                message_id,
                parse_mode=types.ParseMode.HTML,
                reply_markup=keyboard
            )
        except MessageNotModified:
            pass

async def send_cartoon_list(chat_id, message_id, page):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    try:
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
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
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
                    "<b>❌ Ничего не найдено!</b>",
                    chat_id,
                    message_id,
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=keyboard
                )
            except MessageNotModified:
                pass
    except Exception as e:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
        error_message = f"<b>⚠️ Произошла ошибка при обработке запроса. Попробуйте снова позже.</b>\n\n<b>❌ Ошибка:</b> <code>{e}</code>"
        try:
            await bot.edit_message_text(
                error_message,
                chat_id,
                message_id,
                parse_mode=types.ParseMode.HTML,
                reply_markup=keyboard
            )
        except MessageNotModified:
            pass

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    welcome_text = (
        "👋 <b>Добро пожаловать!</b> Я твой виртуальный гид в мире аниме, фильмов, сериалов и мультфильмов.\n\n"
        "🔍 <b>Хочешь найти что-то интересное для просмотра на вечер?</b>\n"
        "Просто напиши мне название аниме, фильма, сериала или мультфильма, "
        "и я помогу тебе отыскать это на Rezka.ag.\n\n"
        "📺 <b>Готов окунуться в приключения?</b>\n"
        "Нажимай на кнопки ниже или отправь мне сообщение, чтобы начать поиск!"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🎬 Аниме", callback_data="search_anime"),
        types.InlineKeyboardButton("🎬 Фильмы", callback_data="search_movies"),
        types.InlineKeyboardButton("🎬 Сериалы", callback_data="search_series"),
        types.InlineKeyboardButton("🎬 Мультфильмы", callback_data="search_cartoons")
    )
    keyboard.add(
        types.InlineKeyboardButton("⭐️ Поддержите нас", callback_data="donate")
    )
    await bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard,
        protect_content=True
    )

@dp.message_handler(commands=["privacy"])
async def cmd_privacy(message: types.Message):
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    privacy_text = (
        f"<b>Политика конфиденциальности @{bot_username}.</b>\n\n"
        f"<b>Дата вступления в силу: 4 июля 2024 г.</b>\n\n"
        f"<b>Добро пожаловать в @{bot_username}!</b> Мы уделяем приоритетное внимание вашей конфиденциальности и стремимся обеспечить защиту ваших личных данных. В данной Политике конфиденциальности описывается, как мы собираем, используем и защищаем вашу информацию в соответствии с рекомендациями <b>Telegram</b>, требованиями <b>Apple App Store</b> и <b>Google Play Store</b>.\n\n"
        f"<b>1. Информация, которую мы собираем:</b>\nДля обеспечения корректной работы нашего бота мы можем собирать следующую информацию из вашего профиля Telegram:\n- ID пользователя (Ваш уникальный идентификатор).\n\n"
        f"<b>2. Как мы используем вашу информацию:</b>\nИнформация, которую мы собираем, используется исключительно с целью предоставления и улучшения наших услуг.\n\n"
        f"<b>3. Хранение и безопасность данных:</b>\n- ID пользователя (Ваш уникальный идентификатор), и связанная с ним информация не сохраняются в базе данных.\n\n"
        f"<b>4. Обмен и продажа данных:</b>\nМы не продаем, не обмениваем и не передаем иным образом вашу личную информацию сторонним лицам. Ваши данные используются исключительно в контексте предоставления вам услуг нашего бота и не передаются никаким сторонним службам.\n\n"
        f"<b>5. Соблюдение требований законодательства:</b>\nМы соблюдаем все соответствующие законодательные требования и отраслевые стандарты, в том числе установленные <b>Telegram</b>, <b>Apple App Store</b> и <b>Google Play Store</b>. Даже в случае юридического обязательства мы не можем раскрыть вашу информацию, если этого требует закон, постановление или судебный процесс, так-как мы не сохраняем ваш уникальный идентификатор в базе данных.\n\n"
        f"<b>6. Изменения в Политике конфиденциальности:</b>\nМы можем время от времени обновлять Политику конфиденциальности, чтобы отражать изменения в нашей практике или юридических требованиях. Любые обновления будут публиковаться на этой странице с указанием даты вступления в силу. Мы рекомендуем вам периодически просматривать Политику конфиденциальности.\n\n"
        f"<b>7. Отказ от ответственности:</b>\nИспользование бота предоставляется пользователю «как есть» в соответствии с общепринятым в международной практике принципом. Это означает, что за проблемы, возникающие в процессе эксплуатации бота (в том числе, но не ограничиваясь, проблемы совместимости с другим программным обеспечением, несоответствия результатов использования бота ожиданиям пользователя, сбои в работе со стороны третьих лиц, и т.п.). Исполнитель ответственности не несет.\n\n"
        f"<b>8. Свяжитесь с нами:</b>\nЕсли у вас есть какие-либо вопросы или сомнения по поводу Политики конфиденциальности или наших методов обработки данных, свяжитесь с нами по адресу <b>@OFFpolice</b>.\n\n"
        f"<b>Используя @{bot_username}, вы соглашаетесь с условиями, изложенными в Политике конфиденциальности.</b>"
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=privacy_text,
        parse_mode=types.ParseMode.HTML,
        protect_content=True
    )

@dp.callback_query_handler(lambda c: c.data.startswith(("search_anime", "search_movies", "search_series", "search_cartoons")))
async def start_search(callback_query: types.CallbackQuery):
    search_texts = {
        "search_anime": "Загружаю страницу «Аниме»",
        "search_movies": "Загружаю страницу «Фильмов»",
        "search_series": "Загружаю страницу «Сериалов»",
        "search_cartoons": "Загружаю страницу «Мультфильмов»"
    }
    search_functions = {
        "search_anime": send_anime_list,
        "search_movies": send_movies_list,
        "search_series": send_series_list,
        "search_cartoons": send_cartoon_list
    }
    await callback_query.answer(search_texts[callback_query.data], show_alert=False)
    await search_functions[callback_query.data](callback_query.message.chat.id, callback_query.message.message_id, page=1)

@dp.callback_query_handler(lambda c: c.data.startswith(("anime_page:", "movie_page:", "series_page:", "cartoon_page:")))
async def process_page_callback(callback_query: types.CallbackQuery):
    search_texts = {
        "anime_page": "Переключаю страницу «Аниме»",
        "movie_page": "Переключаю страницу «Фильмов»",
        "series_page": "Переключаю страницу «Сериалов»",
        "cartoon_page": "Переключаю страницу «Мультфильмов»"
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
        "👋 <b>Добро пожаловать!</b> Я твой виртуальный гид в мире аниме, фильмов, сериалов и мультфильмов.\n\n"
        "🔍 <b>Хочешь найти что-то интересное для просмотра на вечер?</b>\n"
        "Просто напиши мне название аниме, фильма, сериала или мультфильма, "
        "и я помогу тебе отыскать это на Rezka.ag.\n\n"
        "📺 <b>Готов окунуться в приключения?</b>\n"
        "Нажимай на кнопки ниже или отправь мне сообщение, чтобы начать поиск!"
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🎬 Аниме", callback_data="search_anime"),
        types.InlineKeyboardButton("🎬 Фильмы", callback_data="search_movies"),
        types.InlineKeyboardButton("🎬 Сериалы", callback_data="search_series"),
        types.InlineKeyboardButton("🎬 Мультфильмы", callback_data="search_cartoons")
    )
    keyboard.add(
        types.InlineKeyboardButton("⭐️ Поддержите нас", callback_data="donate")
    )
    try:
        await bot.edit_message_text(
            welcome_text,
            callback_query.message.chat.id,
            callback_query.message.message_id,
            parse_mode=types.ParseMode.HTML,
            reply_markup=keyboard
        )
    except MessageNotModified:
        pass

@dp.callback_query_handler(lambda c: c.data == "donate")
async def donate_stars(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("50 ⭐️", callback_data="donate_50"),
        types.InlineKeyboardButton("100 ⭐️", callback_data="donate_100"),
        types.InlineKeyboardButton("150 ⭐️", callback_data="donate_150"),
        types.InlineKeyboardButton("250 ⭐️", callback_data="donate_250"),
        types.InlineKeyboardButton("350 ⭐️", callback_data="donate_350"),
        types.InlineKeyboardButton("500 ⭐️", callback_data="donate_500"),
        types.InlineKeyboardButton("750 ⭐️", callback_data="donate_750"),
        types.InlineKeyboardButton("1000 ⭐️", callback_data="donate_1000"),
    )
    keyboard.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=(
                "<b>Хотите поддержать наш проект?</b>\n\n"
                "<i><u>* Добровольные пожертвования не подразумевают возврат средств!</u></i>\n\n"
                "<b>Выберите сумму для доната:</b>"
            ),
            parse_mode=types.ParseMode.HTML,
            reply_markup=keyboard
        )
    except MessageNotModified:
        pass

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("donate_"))
async def process_donation(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    donation_amount = int(callback_query.data.split("_")[1])

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"Пожертвовать {donation_amount} ⭐️", pay=True))

    await bot.send_invoice(
        chat_id=callback_query.message.chat.id,
        title="Поддержка бота",
        description=f"Вы выбрали сумму: {donation_amount} ⭐️",
        payload=f"donation_{donation_amount}",
        provider_token="",
        currency="XTR", #XTR
        prices=[types.LabeledPrice(label=f"{donation_amount} ⭐️", amount=donation_amount)],
        start_parameter="donation",
        reply_markup=keyboard,
        protect_content=True
    )
    await back_to_main_menu(callback_query)

@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payment_info = message.successful_payment
    amount = payment_info.total_amount
    await message.answer(
        f"🎉 <b>Спасибо за вашу щедрость!</b>\nВы поддержали нас на сумму <code>{amount}</code> ⭐️",
        parse_mode=types.ParseMode.HTML,
        protect_content=True
    )

@dp.message_handler(content_types=[types.ContentType.TEXT])
async def search(message: types.Message):
    if message.via_bot or message.text.startswith('/'):
        return

    name = message.text.strip()
    await bot.send_chat_action(message.chat.id, "typing")
    try:
        title, link = await scraper.search_rezka(name, images=False)
        if title:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                types.InlineKeyboardButton("🍿 Смотреть на Rezka.ag", url=link)
            )
            keyboard.add(
                types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"),
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
            )
            await message.answer(
                f"<b>🎞 Название:</b> <a href=\"{link}\">{title}</a>",
                parse_mode=types.ParseMode.HTML,
                reply_markup=keyboard
            )
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        else:
            await message.answer("<b>❌ Ничего не найдено!</b> Попробуйте изменить запрос или введите другое название.", parse_mode=types.ParseMode.HTML)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        await message.answer(f"<b>⚠️ Произошла ошибка при обработке запроса. Попробуйте снова позже.</b>\n\n<b>❌ Ошибка:</b> <code>{e}</code>", parse_mode=types.ParseMode.HTML)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.inline_handler()
async def inline_search(query: types.InlineQuery):
    name = query.query.strip()
    try:
        if not name:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                types.InlineKeyboardButton("💬 Новый", switch_inline_query=""),
                types.InlineKeyboardButton("💬 Текущий", switch_inline_query_current_chat="")
            )
            keyboard.add(
                types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"),
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
            )
            result = types.InlineQueryResultArticle(
                id="no_query",
                title="🔍 Введите поисковый запрос!",
                description="Введите название аниме, фильма, сериала или мультфильма, для поиска на Rezka.ag.",
                input_message_content=types.InputTextMessageContent(
                    message_text="🔍 Для поиска введите название аниме, фильма, сериала или мультфильма, и я помогу тебе отыскать это на Rezka.ag.",
                    parse_mode=types.ParseMode.HTML
                ),
                reply_markup=keyboard,
                thumb_url="https://i.imgur.com/znbreEu_d.jpeg?maxwidth=520&shape=thumb&fidelity=high"
            )
            await query.answer([result], cache_time=1, is_personal=True, switch_pm_text="Нажмите, чтобы перейти в бота.", switch_pm_parameter="start")
            return

        title, link, image_url = await scraper.search_rezka(name, images=True)
        if title:
            result_id = hashlib.md5(link.encode()).hexdigest()
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                types.InlineKeyboardButton("🍿 Смотреть на Rezka.ag", url=link)
            )
            keyboard.add(
                types.InlineKeyboardButton("💬 Новый", switch_inline_query=""),
                types.InlineKeyboardButton("💬 Текущий", switch_inline_query_current_chat="")
            )
            keyboard.add(
                types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"),
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
            )
            result = types.InlineQueryResultArticle(
                id=result_id,
                title=title,
                description="Нажмите, чтобы посмотреть.",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"<b>🎞 Название:</b> <a href=\"{link}\">{title}</a>",
                    parse_mode=types.ParseMode.HTML
                ),
                reply_markup=keyboard,
                thumb_url=image_url
            )
            await query.answer([result], cache_time=1, is_personal=True, switch_pm_text="Нажмите, чтобы перейти в бота.", switch_pm_parameter="start")
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                types.InlineKeyboardButton("💬 Новый", switch_inline_query=""),
                types.InlineKeyboardButton("💬 Текущий", switch_inline_query_current_chat="")
            )
            keyboard.add(
                types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"),
                types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
            )
            result = types.InlineQueryResultArticle(
                id="no_query",
                title="❌ Ничего не найдено!",
                description="Попробуйте изменить запрос или введите другое название.",
                input_message_content=types.InputTextMessageContent(
                    message_text="<b>❌ Ничего не найдено!</b> Попробуйте изменить запрос или введите другое название.",
                    parse_mode=types.ParseMode.HTML
                ),
                reply_markup=keyboard,
                thumb_url="https://i.imgur.com/znbreEu_d.jpeg?maxwidth=520&shape=thumb&fidelity=high"
            )
            await query.answer([result], cache_time=1, is_personal=True, switch_pm_text="Нажмите, чтобы перейти в бота.", switch_pm_parameter="start")
    except Exception as e:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("💬 Новый", switch_inline_query=""),
            types.InlineKeyboardButton("💬 Текущий", switch_inline_query_current_chat="")
        )
        keyboard.add(
            types.InlineKeyboardButton("🌀 Shazam Bot", url="https://t.me/OFFpoliceShazamBot"),
            types.InlineKeyboardButton("🎞 HDrezka", url="https://t.me/hdrezka_channel")
        )
        result = types.InlineQueryResultArticle(
            id="no_query",
            title="⚠️ Произошла ошибка!",
            description="Произошла ошибка при обработке запроса. Попробуйте снова позже.",
            input_message_content=types.InputTextMessageContent(
                message_text=f"<b>⚠️ Произошла ошибка при обработке запроса. Попробуйте снова позже.</b>\n\n<b>❌ Ошибка:</b> <code>{e}</code>",
                parse_mode=types.ParseMode.HTML
            ),
            reply_markup=keyboard,
            thumb_url="https://i.imgur.com/znbreEu_d.jpeg?maxwidth=520&shape=thumb&fidelity=high"
        )
        await query.answer([result], cache_time=1, is_personal=True, switch_pm_text="Нажмите, чтобы перейти в бота.", switch_pm_parameter="start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
