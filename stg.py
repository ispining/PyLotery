from tools.settings import *


def setLangStage(chat_id):
    k = types.InlineKeyboardMarkup()
    stages(chat_id, "setLang")
    k.row(types.InlineKeyboardButton(f"Русский", callback_data="ru"))
    k.row(types.InlineKeyboardButton(f"English", callback_data="en"))
    send(chat_id, texts.setLangText, reply_markup=k)


def startMessageAfterLang(chat_id):
    k = types.InlineKeyboardMarkup()
    stages(chat_id, "None")
    msg = txt(chat_id, 'startMessageAfterLang')
    start_main_categories(chat_id, k)
    k.row(types.InlineKeyboardButton(buttons(chat_id, 'register'), callback_data='user_register'))
    k.row(types.InlineKeyboardButton(buttons(chat_id, 'reviews'), callback_data='user_reviews_btn'))
    send(chat_id, msg, reply_markup=k)












