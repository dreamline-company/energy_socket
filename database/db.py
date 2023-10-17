"""
    db.py
"""
import os
import logging
import logging.config

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()
logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("db")


def create_server_connection():
    """
    Функция create_server_connection устанавливает соединение
    с базой данных MySQL с помощью модуля mysql.connector.
    """

    connection = None
    try:
        # передаем все данные сервера и открываем соединение
        connection = mysql.connector.connect(
            host=os.getenv("DB_SERVER"),
            user=os.getenv("DB_USERNAME"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
        )
        logger.info(
            "Connected to server '%s' to database named '%s'",
            os.getenv("DB_SERVER"),
            os.getenv("DB_NAME"),
        )
    except Error as err:
        logger.error(err)

    return connection
