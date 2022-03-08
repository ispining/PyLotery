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


def with_docs(chat_id):
    k = kmarkup()
    msg = txt(chat_id, 'with_docs')
    reg_with_docs_buttons(chat_id, k)
    k.row(add_button(chat_id, 'continue', 'continue_reg_docs'))
    k.row(back(chat_id, 'home'))
    send(chat_id, msg, reply_markup=k)
    stages(chat_id, 'None')


def c_panel(chat_id):
        k = kmarkup()
        msg = txt(chat_id, 'c_panel').format(**{'balance': str(balance(chat_id))})
        sellers_group = add_button(chat_id, 'sellers_group',
                        url=bot.export_chat_invite_link(int(DB_setting('sellers_group'))))
        b1 = add_button(chat_id, 'post_ad', 'seller_post_ad')
        b2 = add_button(chat_id, 'my_ads')
        b3 = add_button(chat_id, 'my_channels')
        b4 = add_button(chat_id, 'wallet')
        b5 = add_button(chat_id, 'reviews')
        b6 = add_button(chat_id, 'statistics')
        b7 = add_button(chat_id, 'support', url=str(DB_setting('support_bot')))
        k.row(sellers_group)
        k.row(b1)
        k.row(b2, b3)
        k.row(b4, b5)
        k.row(b6)
        k.row(b7)
        k.row(back(chat_id, 'home'))
        send(chat_id, msg, reply_markup=k)


def my_ads(chat_id):
    k = kmarkup()
    msg = txt(chat_id, 'my_ads')
    sql.execute(f"SELECT * FROM ads WHERE user_id = '{str(chat_id)}'")
    if sql.fetchone() is None:
        k.row(add_button(chat_id, 'add', 'add_ad'))
    else:
        k.row(add_button(chat_id, 'ad_media'), add_button(chat_id, 'edit', 'ad_media_edit'))
        k.row(add_button(chat_id, 'ad_caption'), add_button(chat_id, 'edit', 'ad_caption_edit'))
    k.row(back(chat_id, 'c_panel'))
    send(chat_id, msg, reply_markup=k)
    stages(chat_id, 'None')










