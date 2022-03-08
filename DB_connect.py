import psycopg2

db = psycopg2.connect(database="internat", user="postgres", password="armageddon")
sql = db.cursor()

def commit():
    return db.commit()


def pre_DB():
    sql.execute(f"""CREATE TABLE IF NOT EXISTS lang(
    user_id TEXT,
    lang TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS texts(
    id TEXT,
    ru TEXT,
    en TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS media(
    id TEXT,
    media_type TEXT,
    file_id TEXT,
    file_name TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS sub (
    user_id TEXT,
    sub_date TEXT,
    last_update TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS buttons (
    id TEXT,
    ru TEXT,
    en TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS settings (
    setting TEXT,
    value TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS user_docs (
    user_id TEXT,
    passport TEXT,
    dl TEXT,
    video TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS seller (
    user_id TEXT,
    reg_type TEXT,
    category TEXT,
    status TEXT,
    reg_date TEXT,
    last_post TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS wallet(
    user_id TEXT,
    balance TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS ads(
    user_id TEXT,
    media_type TEXT,
    media_id TEXT,
    caption TEXT,
    switch TEXT
    )""")
    commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS pay_in(
    id TEXT,
    user_id TEXT,
    coins TEXT,
    dollar TEXT,
    tranz TEXT,
    status TEXT,
    time TEXT
    )""")
    commit()



def DB_setting(setting, new_val=None):
    result = None
    sql.execute(f"SELECT * FROM settings WHERE setting = '{str(setting)}'")
    if sql.fetchone() is None:
        pass
    else:
        if new_val != None:
            sql.execute(f"UPDATE settings SET value = '{str(new_val)}' WHERE setting = '{str(setting)}'")
            db.commit()
        sql.execute(f"SELECT * FROM settings WHERE setting = '{str(setting)}'")
        for i in sql.fetchall():
            result = i[1]
    return result


pre_DB()