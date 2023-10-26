""" 
data_raw
"""

import logging
import logging.config
import database.db as db

cnx = db.create_server_connection()

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("data_raw_db_service")


def read_data_raw():
    """
    read_data_raw
    """
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM data_raw")
    data_raw_data = cursor.fetchall()

    cursor.close()

    logger.info("Read from database table 'data_raw'")
    logger.debug("Data from 'data_raw' - %s", data_raw_data)

    return data_raw_data


def create_data_raw(new_data):
    """
    create_data_raw
    """
    cursor = cnx.cursor()
    params_tuple = ",".join(tuple(new_data.keys()))
    values_tuple = tuple(new_data.values())
    insert_symbols = ",".join(tuple((["%s"] * len(new_data.keys()))))

    cursor.execute(
        f"INSERT INTO data_raw ({params_tuple}) VALUES ({insert_symbols})",
        values_tuple,
    )

    cnx.commit()

    cursor.close()

    logger.info("Insert data to database table 'data_raw'")

    return cursor.lastrowid


def update_data_raw(new_data, row_id):
    """
    update_data_raw
    """

    params = [f"{i}={new_data[i]}" for i in new_data.keys()]
    params = ",".join(params)
    
    cursor = cnx.cursor()
    cursor.execute(f"UPDATE data_raw SET {params}  WHERE id = {row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Update data to database table 'data_raw'")

    return cursor.rowcount


def delete_data_raw_by_id(row_id):
    """
    delete_data_raw_by_id
    """

    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM data_raw WHERE id={row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Delete data to database table 'data_raw'")

    return cursor.rowcount