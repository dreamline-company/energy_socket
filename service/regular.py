""" 
regular
"""
import logging
import logging.config
import database.db as db

cnx = db.create_server_connection()

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("regular_db_service")


def read_regular():
    """
    read_regular
    """
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM regular")
    regular_data = cursor.fetchall()

    cursor.close()

    logger.info("Read from database table 'regular'")
    logger.debug("Data from 'regular' - %s", regular_data)

    return regular_data


def create_regular(new_data):
    """
    create_regular
    """
    cursor = cnx.cursor()
    params_tuple = ",".join(tuple(new_data.keys()))
    values_tuple = tuple(new_data.values())
    insert_symbols = ",".join(tuple((["%s"] * len(new_data.keys()))))
    print(f"INSERT INTO regular ({params_tuple}) VALUES ({insert_symbols})", values_tuple,)
    cursor.execute(
        f"INSERT INTO regular ({params_tuple}) VALUES ({insert_symbols})",
        values_tuple,
    )

    cnx.commit()

    cursor.close()

    logger.info("Insert data to database table 'regular'")

    return cursor.lastrowid


def update_regular(new_data, row_id):
    """
    update_regular
    """

    params = [f"{i}={new_data[i]}" for i in new_data.keys()]
    params = ",".join(params)
    
    cursor = cnx.cursor()
    cursor.execute(f"UPDATE regular SET {params}  WHERE id = {row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Update data to database table 'regular'")

    return cursor.rowcount


def delete_regular_by_id(row_id):
    """
    delete_regular_by_id
    """

    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM regular WHERE id={row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Delete data to database table 'regular'")

    return cursor.rowcount
