""" 
general
"""
import logging
import logging.config
import database.db as db

cnx = db.create_server_connection()

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("general_db_service")


def read_general():
    """
    read_general
    """
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM general")
    general_data = cursor.fetchall()

    cursor.close()

    logger.info("Read from database table 'general'")
    logger.debug("Data from 'general' - %s", general_data)

    return general_data


def create_general(new_data):
    """
    create_general
    """
    cursor = cnx.cursor()
    params_tuple = ",".join(tuple(new_data.keys()))
    values_tuple = tuple(new_data.values())
    insert_symbols = ",".join(tuple((["%s"] * len(new_data.keys()))))

    cursor.execute(
        f"INSERT INTO general ({params_tuple}) VALUES ({insert_symbols})",
        values_tuple,
    )

    cnx.commit()

    cursor.close()

    logger.info("Insert data to database table 'general'")

    return cursor.lastrowid


def update_general(new_data, row_id):
    """
    update_general
    """

    params = [f"{i}={new_data[i]}" for i in new_data.keys()]
    params = ",".join(params)
    
    cursor = cnx.cursor()
    cursor.execute(f"UPDATE general SET {params}  WHERE id = {row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Update data to database table 'general'")

    return cursor.rowcount


def delete_general_by_id(row_id):
    """
    delete_general_by_id
    """

    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM general WHERE id={row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Delete data to database table 'general'")

    return cursor.rowcount
