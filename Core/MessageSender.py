
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Message, CallbackQuery

from main import bot
from Core.StorageManager.UniqueMessagesKeys import textConstant
from logger import logger as log

class MessageSender:

    async def answer(self, ctx: Message, text: str, inlineMarkup: InlineKeyboardMarkup):

        log.debug(f"MessageSender sends: {text}")
        await ctx.answer(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=inlineMarkup
        )

    async def answer(self, ctx: Message, text: str, keyboardMarkup: ReplyKeyboardMarkup):
        
        await ctx.answer(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboardMarkup
        )

    async def answerUnknown(self, ctx: Message):

        nknownText = textConstant.unknownState.get()
        await ctx.answer(
            nknownText,
            parse_mode=ParseMode.MARKDOWN
        )

class MessageSenderAdmin(MessageSender):

    async def answer(self, ctx: Message, text: str, keyboardMarkup: ReplyKeyboardMarkup):
        
        await ctx.answer(
            text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboardMarkup.add(KeyboardButton(textConstant.adminButtonText.get()))
        )