from config import TOKEN
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import random
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keybutton = [
        [InlineKeyboardButton("🎲 Бросить кубик (1-6)", callback_data='dice')],
        [InlineKeyboardButton("🪙 Подбросить монету", callback_data='flip')],
        [InlineKeyboardButton("🔢 Случайное число (1-100)", callback_data='random')],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keybutton)

    if update.message:
        await update.message.reply_text(
            f"Привет, {user.first_name}👋\nВыбери игру:",
            reply_markup=reply_markup
        )
    else:
        await update.callback_query.edit_message_text(
            f"Привет, {user.first_name}👋\nВыбери игру:",
            reply_markup=reply_markup
        )
    
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'dice':
        await dice(update, context)
    elif query.data == 'flip':
        await flip_animation(update, context)
    elif query.data == 'random':
        await random_cmd(update, context)
    elif query.data == 'help':
        await help_command(update, context)
    elif query.data == 'start':
        await start(update, context)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Доступные команды:\n"
           "/dice - бросить кубик (1-6)\n"
           "/flip - подбросить монету\n"
           "/random - случайное число (1-100)\n"
           "/help - помощь")
    
    if update.message:
        await update.message.reply_text(text)
    else:
        await update.callback_query.message.reply_text(text)

# Команда /dice
async def dice_animation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_value = random.randint(1, 6)
    keybutton = [
        [InlineKeyboardButton("Еще раз 🔁", callback_data='dice')],
        [InlineKeyboardButton("⏪ Вернуться", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keybutton)

    animation_frames = [
        "🎲 Кубик подбрасывается...",
        f"🎲 Выпало: {dice_value}"
    ]
    
    if update.message:
        message = await update.message.reply_text(animation_frames[0])
        for frame in animation_frames[1:-1]:
            await message.edit_text(frame)
        await asyncio.sleep(0.5)
        await message.edit_text(animation_frames[-1], reply_markup=reply_markup)
    else:
        query = update.callback_query
        for frame in animation_frames:
            await query.edit_message_text(frame)
            await asyncio.sleep(0.5)
        await query.edit_message_text(animation_frames[-1], reply_markup=reply_markup)
   
    
async def random_cmd_animation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_value = random.randint(1, 100)
    keybutton = [
        [InlineKeyboardButton("Еще раз 🔁", callback_data='random')],
        [InlineKeyboardButton("⏪ Вернуться", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keybutton)

    animation_frames = [
        "🔢 Число генерируется...",
        f"🔢 Выпало: {random_value}"
    ]
    
    if update.message:
        message = await update.message.reply_text(animation_frames[0])
        for frame in animation_frames[1:-1]:
            await message.edit_text(frame)
        await asyncio.sleep(0.5)
        await message.edit_text(animation_frames[-1], reply_markup=reply_markup)
    else:
        query = update.callback_query
        for frame in animation_frames:
            await query.edit_message_text(frame)
            await asyncio.sleep(0.5)
        await query.edit_message_text(animation_frames[-1], reply_markup=reply_markup)

# Анимированное подбрасывание монетки
async def flip_animation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flip_value = random.choice(["Орёл", "Решка"])
    keybutton = [
        [InlineKeyboardButton("Еще раз 🔁", callback_data='flip')],
        [InlineKeyboardButton("⏪ Вернуться", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keybutton)
    
    animation_frames = [
        "🪙 Монета подбрасывается...",
        f"🪙 Выпало: {flip_value}"
    ]
    
    if update.message:
        message = await update.message.reply_text(animation_frames[0])
        for frame in animation_frames[1:-1]:
            await message.edit_text(frame)
        await asyncio.sleep(0.5)
        await message.edit_text(animation_frames[-1], reply_markup=reply_markup)
    else:
        query = update.callback_query
        for frame in animation_frames:
            await query.edit_message_text(frame)
            await asyncio.sleep(0.5)
        await query.edit_message_text(animation_frames[-1], reply_markup=reply_markup)

# Обычное подбрасывание монетки (без анимации)
async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await flip_animation(update, context)

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await dice_animation(update, context)

async def random_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await random_cmd_animation(update, context)



def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("random", random_cmd))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("flip", flip))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    #запуск 
    application.run_polling()

if __name__ == '__main__':
    main()