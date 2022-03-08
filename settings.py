import os
import threading
from . import texts

from .lang import *
from .config import *


MEDIA_PATH = os.getcwd()+'\\medias\\'

def media_path(file_name):
    return MEDIA_PATH + str(file_name)


def switch(switch, status=None):
    result = None
    sql.execute(f"SELECT * FROM switches WHERE switch = '{str(switch)}'")
    if sql.fetchone() is None:
        if status != None:
            sql.execute(f"INSERT INTO switches VALUES('{str(switch)}', '{str(status)}')")
            commit()
    else:
        if status != None:
            sql.execute(f"UPDATE switches SET status = '{str(status)}' WHERE switch = '{str(switch)}'")
            commit()
        sql.execute(f"SELECT * FROM switches WHERE switch = '{str(switch)}'")
        for i in sql.fetchall():
            result = i[1]
            if result == 'True':
                return True
            else:
                return False


def dollars_to_BTC(dollars):
    import requests
    r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = r.json()
    bitprice = data["bpi"]["USD"]["rate"]
    bitprice = bitprice.replace(',', '')

    return round(int(dollars) / float(bitprice), 8)


def start_new_thread(target):
    polling_thread = threading.Thread(target=target)
    polling_thread.daemon = True
    polling_thread.start()


def staff(user_id, status=None, remove=False):
    sql.execute(f"""CREATE TABLE IF NOT EXISTS staff(
       user_id TEXT,
       status TEXT
       )""")
    db.commit()
    if status == None:
        if remove == False:
            s = None
            sql.execute(f"SELECT * FROM staff WHERE user_id = '{str(user_id)}'")
            if sql.fetchone() is None:
                pass
            else:
                sql.execute(f"SELECT * FROM staff WHERE user_id = '{str(user_id)}'")
                for i in sql.fetchall():
                    s = i[1]
            return s
        elif remove == True:
            sql.execute(f"SELECT * FROM staff WHERE user_id = '{str(user_id)}'")
            if sql.fetchone() is None:
                pass
            else:
                sql.execute(f"DELETE FROM staff WHERE user_id = '{str(user_id)}'")
                db.commit()
    elif status != None:
        sql.execute(f"SELECT * FROM staff WHERE user_id = '{str(user_id)}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO staff VALUES('{str(user_id)}','{str(status)}')")
            db.commit()
        else:
            sql.execute(f"UPDATE staff SET status = '{str(status)}' WHERE user_id = '{str(user_id)}'")
            db.commit()


def distance(lat1, lon1, lat2, lon2):
    from geopy.distance import great_circle
    locationA = (lat1, lon1)
    locationB = (lat2, lon2)
    return round(great_circle.geodesic(locationA, locationB).km, 3)


def stages(user_id, stage=None):
    sql.execute(f"""CREATE TABLE IF NOT EXISTS stages(
    user_id TEXT,
    stage TEXT
    )""")
    db.commit()
    if stage == None:
        s = "None"
        sql.execute(f"SELECT * FROM stages WHERE user_id = '{str(user_id)}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO stages VALUES('{str(user_id)}','{s}')")
            db.commit()
        else:
            sql.execute(f"SELECT * FROM stages WHERE user_id = '{str(user_id)}'")
            for i in sql.fetchall():
                s = i[1]
        return s

    elif stage != None:
        sql.execute(f"SELECT * FROM stages WHERE user_id = '{str(user_id)}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO stages VALUES('{str(user_id)}','{str(stage)}')")
            db.commit()
        else:
            sql.execute(f"UPDATE stages SET stage = '{str(stage)}' WHERE user_id = '{str(user_id)}'")
            db.commit()


def mediaFile(media_id):
    sql.execute(f"""CREATE TABLE IF NOT EXISTS media(
    id TEXT,
    media_type TEXT,
    file_id TEXT,
    file_name TEXT
    )""")
    commit()
    sql.execute(f"SELECT * FROM media WHERE id = '{media_id}'")
    for m in sql.fetchall():
        if m[2] == 'None':
            return [m[1], m[3]]  #type, path
        else:
            return [m[1], m[2]]  #type, id


def send_media(chat_id, media_id, caption=None, reply_markup=None, disable_notification=False):
    sql.execute(f"SELECT * FROM media WHERE id = '{media_id}'")
    for m in sql.fetchall():
        if m[2] == 'None':
            file = os.getcwd()+'\\media\\'+ mediaFile(media_id)[1]  #path
            ofile = open(file, "rb")
            if mediaFile(media_id)[0] == 'photo':
                sendedMSG = bot.send_photo(chat_id=chat_id, photo=ofile, caption=caption, reply_markup=reply_markup, disable_notification=disable_notification, timeout=20000)
                file_id = sendedMSG.photo[-1].file_id
                sql.execute(f"UPDATE media SET file_id = '{str(file_id)}' WHERE id = '{str(m[0])}'")
                commit()

            elif mediaFile(media_id)[0] == 'video':
                sendedMSG = bot.send_video(chat_id=chat_id, data=ofile, caption=caption, reply_markup=reply_markup, disable_notification=disable_notification,timeout=20000)
                file_id = sendedMSG.video.file_id
                sql.execute(f"UPDATE media SET file_id = '{str(file_id)}' WHERE id = '{str(m[0])}'")
                commit()

        else:
            if mediaFile(media_id)[0] == 'photo':
                bot.send_photo(chat_id=chat_id, photo=m[2], caption=caption, reply_markup=reply_markup, disable_notification=disable_notification)
            elif mediaFile(media_id)[0] == 'video':
                bot.send_video(chat_id=chat_id, data=m[2], caption=caption, reply_markup=reply_markup, disable_notification=disable_notification)


def send(chat_id, msg, reply_markup=None, disable_notification=False):
    bot.send_message(chat_id, msg, reply_markup=reply_markup, disable_notification=disable_notification, parse_mode='HTML')


def start_main_categories(chat_id, k):
    k.row(types.InlineKeyboardButton(buttons(chat_id, 'card_cat'), url='card_cat'))
    k.row(types.InlineKeyboardButton(buttons(chat_id, 'baza_cat'), url='baza_cat'))
    k.row(types.InlineKeyboardButton(buttons(chat_id, 'hack_cat'), url='hack_cat'))


def kmarkup():
    return types.InlineKeyboardMarkup()


def back(user_id, callback_data):
    return types.InlineKeyboardButton(buttons(user_id, 'back'), callback_data=callback_data)


def add_button(user_id, button_id, callback_data=None, url=None):
    if callback_data == None and url == None:
        return types.InlineKeyboardButton(buttons(user_id, str(button_id)), callback_data=button_id)
    elif callback_data != None and url == None:
        return types.InlineKeyboardButton(buttons(user_id, str(button_id)), callback_data=callback_data)
    elif callback_data == None and url != None:
        return types.InlineKeyboardButton(buttons(user_id, str(button_id)), url=str(url))


def check_seller_docs(user_id):
    sql.execute(f"SELECT * FROM user_docs WHERE user_id = '{user_id}'")
    if sql.fetchone() is None:
        return {'passport': 'None',
                'dl': 'None',
                'video': 'None'}
    else:
        sql.execute(f"SELECT * FROM user_docs WHERE user_id = '{user_id}'")
        for i in sql.fetchall():
            return {'passport': i[1],
                    'dl': i[2],
                    'video': i[3]}


def reg_with_docs_buttons(user_id, k):

    if check_seller_docs(user_id)['passport'] != 'None':
        k.row(add_button(user_id, 'y_passport_doc', 'passport_doc1'))  # passport (doc1)
    else:
        k.row(add_button(user_id, 'n_passport_doc', 'passport_doc1'))  # passport (doc1)

    if check_seller_docs(user_id)['dl'] != 'None':
        k.row(add_button(user_id, 'y_dl', 'passport_doc2'))  # driver licence (doc2)
    else:
        k.row(add_button(user_id, 'n_dl', 'passport_doc2'))  # driver licence (doc2)

    if check_seller_docs(user_id)['video'] != 'None':
        k.row(add_button(user_id, 'y_video_doc', 'video_doc3'))  # video_selfie
    else:
        k.row(add_button(user_id, 'n_video_doc', 'video_doc3'))  # video_selfie


def down_file(file_id, name):
    file_info = bot.get_file(file_id)

    downloaded_file = bot.download_file(file_info.file_path)


    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    return {'file_id': file_id,
            'status': 200}


def get_username(message):
        return message.from_user.get_username


# ['photo1' / 'photo2' / 'video']
def get_reg_docs(user_id):
    sql.execute(f"SELECT * FROM user_docs WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        return {
            'photo1': 'None',
            'photo2': 'None',
            'video': 'None'
        }
    else:
        sql.execute(f"SELECT * FROM user_docs WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            return {
                'photo1': i[1],
                'photo2': i[2],
                'video': i[3]
            }


def create_new_seller(user_id):
    sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO seller VALUES('{str(user_id)}','None','None','None','None','None')")
        commit()


def seller_reg_type(user_id, new=None):
    sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        pass
    else:
        if new != None:
            sql.execute(f"UPDATE seller SET reg_type = '{str(new)}' WHERE user_id = '{str(user_id)}'")
            commit()
        sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            return i[1]


def seller_category(user_id, new=None):
    sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        pass
    else:
        if new != None:
            sql.execute(f"UPDATE seller SET category = '{str(new)}' WHERE user_id = '{str(user_id)}'")
            commit()
        sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            return i[2]


def seller_status(user_id, new=None):
    sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        pass
    else:
        if new != None:
            sql.execute(f"UPDATE seller SET status = '{str(new)}' WHERE user_id = '{str(user_id)}'")
            commit()
        sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            return i[3]


def seller_reg_date(user_id, new=None):
    sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        pass
    else:
        if new != None:
            sql.execute(f"UPDATE seller SET reg_date = '{str(new)}' WHERE user_id = '{str(user_id)}'")
            commit()
        sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            return i[4]


def seller_last_post(user_id, new=None):
    sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        pass
    else:
        if new != None:
            sql.execute(f"UPDATE seller SET last_post = '{str(new)}' WHERE user_id = '{str(user_id)}'")
            commit()
        sql.execute(f"SELECT * FROM seller WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            return i[4]


def balance(user_id, new=None):
    result = 0
    sql.execute(f"SELECT * FROM wallet WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        if new != None:
            sql.execute(f"INSERT INTO wallet VALUES('{str(user_id)}', '{str(new)}')")
            commit()
    else:
        if new != None:
            sql.execute(f"UPDATE wallet SET balance = '{str(new)}' WHERE user_id = '{str(user_id)}'")
            commit()
        sql.execute(f"SELECT * FROM wallet WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            result = int(i[1])
    return result


def ad_text_checker(text):
    t_list = text.split()
    if '@' in t_list:
        pass
    else:
        return text


def pay_in(user_id, pay_id, coins=None, dollar=None, tranz=None, status=None, time=None):
    def create():
        sql.execute(f"INSERT INTO pay_in VALUES('{str(user_id)}', '{str(pay_id)}', 'None', 'None', 'None', 'None', 'None')")
        commit()

    def update():
        if coins != None:
            sql.execute(f"UPDATE coins = '{str(coins)}' WHERE user_id = '{str(user_id)}' AND id = '{str(pay_id)}'")
            commit()
        if dollar != None:
            sql.execute(f"UPDATE dollar = '{str(dollar)}' WHERE user_id = '{str(user_id)}' AND id = '{str(pay_id)}'")
            commit()
        if tranz != None:
            sql.execute(f"UPDATE tranz = '{str(tranz)}' WHERE user_id = '{str(user_id)}' AND id = '{str(pay_id)}'")
            commit()
        if status != None:
            sql.execute(f"UPDATE status = '{str(status)}' WHERE user_id = '{str(user_id)}' AND id = '{str(pay_id)}'")
            commit()
        if time != None:
            sql.execute(f"UPDATE time = '{str(time)}' WHERE user_id = '{str(user_id)}' AND id = '{str(pay_id)}'")
            commit()

    sql.execute(f"SELECT * FROM pay_in WHERE user_id = '{str(user_id)}' AND id = '{str(pay_id)}'")
    if sql.fetchone() is None:
        create()
        update()
    else:
        update()

    sql.execute(f"SELECT * FROM pay_in WHERE user_id = '{str(user_id)}' AND id = '{str(pay_id)}'")
    for i in sql.fetchall():
        return {
            'id': i[0],
            'user_id': i[1],
            'coins': i[2],
            'dollar': i[3],
            'tranz': i[4],
            'status': i[5],
            'time': i[6]
        }


def del_from_dbs():
    sql.execute(f"DELETE FROM pay_in WHERE status = 'None'")
    commit()