import sqlite3
import logging


def connect():
    global connection, cursor
    connection = sqlite3.connect("numbers.db")
    cursor = connection.cursor()
    if connection:
        logging.info("Connected to database")
    cursor.execute('CREATE TABLE IF NOT EXISTS numbers(num TEXT, lang TEXT, file_id TEXT)')
    connection.commit()


async def add_num(num, lang, file_id):
    cursor.execute('INSERT INTO numbers VALUES (?, ?, ?)', (num, lang, file_id))
    connection.commit()


async def get_num(num, lang):
    cursor.execute('SELECT file_id FROM numbers WHERE num=? AND lang=?', (num, lang))
    fileid = cursor.fetchone()
    if fileid is not None:
        fileid = fileid[0]
    return fileid


def close():
    connection.close()
    logging.info("Connection to database closed")
