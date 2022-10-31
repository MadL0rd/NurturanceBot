

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Message, CallbackQuery

from logger import logger as log

import MenuModules.MenuDispatcher as dispatcher

#Импорты для рандомных картинок. Да, это комменты на русском, и хуле ты мне сделаешь?!
from glob import glob
from random import choice

apiKey = "5659838410:AAEw9C4HuJs5R_wlzFpXeldJPk1N9ELLez4"

# Initialize bot and dispatcher
bot = Bot(token=apiKey)
dp = Dispatcher(bot)


class ButtonsCoufiguration:
    give_me_task = "Перейти к упражнениям"

buttons = ButtonsCoufiguration()

keyboard_markup_wallet_does_not_connected = ReplyKeyboardMarkup(
        resize_keyboard=True
    ).add(KeyboardButton(buttons.give_me_task))

emotion_rate = InlineKeyboardMarkup(
    
    inline_keyboard=[
        [
            InlineKeyboardButton(text="0", callback_data='{ "kek": "sdfs", "dsf": 12334 }')
        ],
        [
            InlineKeyboardButton(text="kek", callback_data='emotion_rate_3')
        ]
    ]
)

# =====================
# Bot commands
# =====================

async def msg(ctx, text: str):
    reply_markup = keyboard_markup_wallet_does_not_connected

    if text != '':
        await ctx.answer(text,
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=emotion_rate)
    else:
        ctx.reply_text('How can I help?', reply_markup=reply_markup)

@dp.message_handler(commands=['start'])
async def send_welcome_message_handler(message: types.Message):
    await dispatcher.handleUserStart(message)
    await msg(message, f'Привет, {message.from_user.first_name}!')

@dp.message_handler()
async def default_message_handler(message: Message):
    await dispatcher.handleUserMessage(message)

@dp.callback_query_handler()
async def default_callback_handler(ctx: CallbackQuery):
    await dispatcher.handleCallback(ctx)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

log.info("Bot just started")