""" 
emergency
"""
import logging
import logging.config
import database.db as db


logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("emergency_db_service")


def read_emergency():
    """
    read_emergency
    """
    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM emergency")
    emergency_data = cursor.fetchall()

    cursor.close()

    logger.info("Read from database table 'emergency'")
    logger.debug("Data from 'emergency' - %s", emergency_data)

    return emergency_data


def create_emergency(new_data):
    """
    create_emergency
    """
    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    params_tuple = ",".join(tuple(new_data.keys()))
    values_tuple = tuple(new_data.values())
    insert_symbols = ",".join(tuple((["%s"] * len(new_data.keys()))))

    cursor.execute(
        f"INSERT INTO emergency ({params_tuple}) VALUES ({insert_symbols})",
        values_tuple,
    )

    cnx.commit()
    print(new_data)
    for key in new_data.keys():
        print(key, new_data[key])
        if new_data[key] != 0:
            signal = "{0:b}".format(new_data[key])
            ind = 1
            print(signal)
            for c in signal[::-1]:
                if c == '1':
                    print('ind -- ', ind)
        else:
            pass
            cursor.execute()

    cursor.close()

    logger.info("Insert data to database table 'emergency'")

    return cursor.lastrowid


def update_emergency(new_data, row_id):
    """
    update_emergency
    """

    params = [f"{i}={new_data[i]}" for i in new_data.keys()]
    params = ",".join(params)
    
    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    cursor.execute(f"UPDATE emergency SET {params}  WHERE id = {row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Update data to database table 'emergency'")

    return cursor.rowcount


def delete_emergency_by_id(row_id):
    """
    delete_emergency_by_id
    """

    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM emergency WHERE id={row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Delete data to database table 'emergency'")

    return cursor.rowcount
