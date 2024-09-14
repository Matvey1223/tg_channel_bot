import asyncio
import sqlite3

def create_users_table():
    with sqlite3.connect('database.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT)')
        db.commit()

def create_sources_table():
    with sqlite3.connect('database.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY)')
        db.commit()

def create_news_table():
    with sqlite3.connect('database.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS news (url TEXT UNIQUE, text TEXT, image TEXT)')
        db.commit()

def create_news_gpt_table():
    with sqlite3.connect('database.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS news_gpt (url TEXT, gpt TEXT)')
        db.commit()

def add_user(user_id, username):
    with sqlite3.connect('database.db') as db:
        db.execute('INSERT OR IGNORE INTO users VALUES (?, ?)', (user_id, username))
        db.commit()


def add_source(url):
    with sqlite3.connect('database.db') as db:
        db.execute('INSERT OR IGNORE INTO sources VALUES (?)', (url,))
        db.commit()


def select_sources():
    with sqlite3.connect('database.db') as db:
        cursor = db.execute('SELECT * FROM sources')
        row = cursor.fetchall()
    return row

def add_new(url, new, img):
    with sqlite3.connect('database.db') as db:
        db.execute('INSERT INTO news VALUES (?, ?, ?)', (url, new, img))
        db.commit()

def select_news():
    with sqlite3.connect('database.db') as db:
        cursor = db.execute('SELECT * FROM news')
        row = cursor.fetchall()
    return row

def clear_news_table():
    with sqlite3.connect('database.db') as db:
        db.execute('DELETE FROM news')
        db.commit()



def add_new_gpt(url, new):
    with sqlite3.connect('database.db') as db:
        db.execute('INSERT INTO news_gpt VALUES (?, ?)', (url, new))
        db.commit()

def select_news_gpt():
    with sqlite3.connect('database.db') as db:
        cursor = db.execute('SELECT * FROM news_gpt')
        row = cursor.fetchall()
    return row

def clear_news_gpt():
    with sqlite3.connect('database.db') as db:
        db.execute('DELETE FROM news_gpt')
        db.commit()