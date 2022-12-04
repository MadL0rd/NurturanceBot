import itertools
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from logger import logger as log
import platform

isWindows = platform.system() == 'Windows'

def groupListToPairs(source: list):
    result = []
    source = source.copy()
    while len(source) > 0:
        if len(source) > 1:
            result.append([source[0], source[1]])
            del source[0]
            del source[0]
        else:
            result.append([source[0]])
            del source[0]
    return result

def replyMarkupFromListOfLines(lines: list) -> ReplyKeyboardMarkup:
    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    for line in lines:
        if len(line) > 1:
            keyboardMarkup.row(
                KeyboardButton(line[0]),
                KeyboardButton(line[1])
            )
        else:
            keyboardMarkup.row(
                KeyboardButton(line[0])
            )

    return keyboardMarkup

def replyMarkupFromListOfButtons(buttons: list, twoColumns: bool = True) -> ReplyKeyboardMarkup:
    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    if len(buttons) > 4 and twoColumns == True:
        pairs = groupListToPairs(buttons)
        return replyMarkupFromListOfLines(pairs)

    for buttonText in buttons:
        keyboardMarkup.row(
            KeyboardButton(buttonText)
        )

    return keyboardMarkup

def quantityOfVariants(list:list):
    # its a quantity of variants for list
    return int((len(list)-2)/2)
