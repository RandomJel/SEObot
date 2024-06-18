import os
import logging
from telegram import Update, BotCommand, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext

# Получите ваш API токен для Telegram
TELEGRAM_BOT_TOKEN = ''

# Замените на пути к вашим изображениям
IMAGE_PATHS = {
    "посещаемость сайта": "D:\Диплом\Мой диплом\Статистика с сайта\прирост посещаемости.png",
    "источники трафика": "D:\Диплом\Мой диплом\Статистика с сайта\Источники трафика.png",
    "новые и вернувшиеся пользователи": "D:\Диплом\Мой диплом\Статистика с сайта\Вернувшиеся пользователи.png",
    "время на сайте": "D:\Диплом\Мой диплом\Статистика с сайта\Время просмотра.png",
    "отказы": "D:\Диплом\Мой диплом\Статистика с сайта\Отказы.png",
    "глубина просмотра": "D:\Диплом\Мой диплом\Статистика с сайта\Глубина просмотра.png",
}

# Инициализация бота
async def set_commands_to_start(bot):
    await bot.set_my_commands([
        BotCommand("/start", "Запустить бота"),
        BotCommand("/help", "Список команд"),
        BotCommand("/stats", "Получить SEO статистику")
    ])

# Меню
def show_menu():
    # Создаем клавиатуру
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item_stats = KeyboardButton('Получить SEO статистику')
    item_help = KeyboardButton('Помощь')
    
    # Добавляем кнопки на клавиатуру
    markup.add(item_stats, item_help)

    return markup

# /start
async def start(update: Update, context: CallbackContext):
    bot = context.bot
    await set_commands_to_start(bot)
    markup = show_menu()
    await update.message.reply_text("Привет! Напиши /help, чтобы узнать, что я умею.", reply_markup=markup)

# /help
async def help(update: Update, context: CallbackContext):
    await update.message.reply_text("""*И так... я умею*: 
- _Предоставляю статистику по SEO_

Команды:
/start - запустить бота
/stats - получить SEO статистику
""", parse_mode='markdown')

# /stats
async def stats(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Посещаемость сайта", callback_data='посещаемость сайта')],
        [InlineKeyboardButton("Источники трафика", callback_data='источники трафика')],
        [InlineKeyboardButton("Новые и вернувшиеся пользователи", callback_data='новые и вернувшиеся пользователи')],
        [InlineKeyboardButton("Время на сайте", callback_data='время на сайте')],
        [InlineKeyboardButton("Отказы", callback_data='отказы')],
        [InlineKeyboardButton("Глубина просмотра", callback_data='глубина просмотра')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите показатель:', reply_markup=reply_markup)

# Обработчик выбора категории статистики
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    selection = query.data

    image_path = IMAGE_PATHS.get(selection)
    if image_path:
        with open(image_path, 'rb') as photo:
            await query.message.reply_photo(photo=photo, caption=f"Вот данные пункта: {selection}")

def main():
    # Инициализация логирования
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelень)s - %(message)s',
                        level=logging.INFO)

    # Инициализация бота и получение токена
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация обработчика команды /start
    application.add_handler(CommandHandler('start', start))
    # Регистрация обработчика команды /help
    application.add_handler(CommandHandler('help', help))
    # Регистрация обработчика команды /stats
    application.add_handler(CommandHandler('stats', stats))
    # Регистрация обработчика нажатий на кнопки
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
