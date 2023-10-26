""" 
tx_config
"""

import logging
import logging.config
import database.db as db

cnx = db.create_server_connection()

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("tx_config_db_service")


def read_tx_config():
    """
    read_tx_config
    """
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM tx_config")
    tx_config_data = cursor.fetchall()

    cursor.close()

    logger.info("Read from database table 'tx_config'")
    logger.debug("Data from 'tx_config' - %s", tx_config_data)

    return tx_config_data


def read_unsended_tx_config(obj_id):
    """
    read_unsended_tx_config
    """
    cursor = cnx.cursor()
    # запускаем SQL запрос
    cursor.execute(
        f"SELECT * FROM tx_config WHERE obj_num={obj_id} AND dt_2 IS NULL ORDER BY dt_1 ASC LIMIT 1"
    )

    # Извлекаем имя из ответа базы данных
    state = cursor.fetchall()
    # Фиксируем данные в базе данных

    cnx.commit()
    cursor.close()
    return state


def create_tx_config(new_data):
    """
    create_tx_config
    """
    cursor = cnx.cursor()
    params_tuple = ",".join(tuple(new_data.keys()))
    values_tuple = tuple(new_data.values())
    insert_symbols = ",".join(tuple((["%s"] * len(new_data.keys()))))

    cursor.execute(
        f"INSERT INTO tx_config ({params_tuple}) VALUES ({insert_symbols})",
        values_tuple,
    )

    cnx.commit()

    cursor.close()

    logger.info("Insert data to database table 'tx_config'")

    return cursor.lastrowid


def update_tx_config(new_data, row_id):
    """
    update_tx_config
    """

    params = [f"{i}={new_data[i]}" for i in new_data.keys()]
    params = ",".join(params)
    
    cursor = cnx.cursor()
    cursor.execute(f"UPDATE tx_config SET {params}  WHERE id = {row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Update data to database table 'tx_config'")

    return cursor.rowcount

def update_dt_2_tx_config(row_id):
    """
    update_tx_config
    """

    params = [f"{i}={new_data[i]}" for i in new_data.keys()]
    params = ",".join(params)
    
    cursor = cnx.cursor()
    cursor.execute(f"UPDATE tx_config SET dt_2 = NOW() WHERE id = {row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Update data to database table 'tx_config'")

    return cursor.rowcount


def delete_tx_config_by_id(row_id):
    """
    delete_tx_config_by_id
    """

    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM tx_config WHERE id={row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Delete data to database table 'tx_config'")

    return cursor.rowcount