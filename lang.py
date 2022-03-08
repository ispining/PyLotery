from .DB_connect import *



def lang(user_id, new=None):
    result = None
    sql.execute(f"SELECT * FROM lang WHERE user_id = '{str(user_id)}'")
    if sql.fetchone() is None:
        if new != None:
            sql.execute(f"INSERT INTO lang VALUES ('{str(user_id)}', '{str(new)}')")
            db.commit()
            return new
    else:
        if new != None:
            sql.execute(f"UPDATE lang SET lang = '{str(new)}' WHERE user_id = '{str(user_id)}'")
            db.commit()
        sql.execute(f"SELECT * FROM lang WHERE user_id = '{str(user_id)}'")
        for i in sql.fetchall():
            result = i[1]

    return result



def txt(user_id, txt_id):
    sql.execute(f"SELECT * FROM texts WHERE id = '{str(txt_id)}'")
    for i in sql.fetchall():
        if lang(user_id) == 'ru':
            return i[1]
        elif lang(user_id) == 'en':
            return i[2]

def buttons(user_id, btn_id):
    sql.execute(f"SELECT * FROM buttons WHERE id = '{str(btn_id)}'")
    for i in sql.fetchall():
        if lang(user_id) == 'ru':
            return i[1]
        elif lang(user_id) == 'en':
            return i[2]