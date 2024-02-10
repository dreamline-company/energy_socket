""" 
regular
"""
import logging
import logging.config
import database.db as db


logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger("regular_db_service")


def read_regular():
    """
    read_regular
    """
    cnx = db.create_server_connection()
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
    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    params_tuple = ",".join(tuple(new_data.keys()))
    values_tuple = tuple(new_data.values())
    insert_symbols = ",".join(tuple((["%s"] * len(new_data.keys()))))

    currentA = 0
    currentB = 0
    currentC = 0
    currentD = 0
    freq = 0

    if '`0030`' in new_data and '`0031`' in new_data:
        regs = [new_data['`0030`'], new_data['`0031`']]
        tmp = ""
        for i in range(0, 16 - len(bin(regs[0])[2:])):
            tmp += "0"
        tmp += bin(regs[0])[2:]
        currentA = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`0032`' in new_data and '`0033`' in new_data:
        regs = [new_data['`0032`'], new_data['`0033`']]
        tmp = ""
        for i in range(0, 16 - len(bin(regs[0])[2:])):
            tmp += "0"
        tmp += bin(regs[0])[2:]
        currentB = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`0034`' in new_data and '`0035`' in new_data:
        regs = [new_data['`0034`'], new_data['`0035`']]
        tmp = ""
        for i in range(0, 16 - len(bin(regs[0])[2:])):
            tmp += "0"
        tmp += bin(regs[0])[2:]
        currentC = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`0036`' in new_data and '`0037`' in new_data:
        regs = [new_data['`0036`'], new_data['`0037`']]
        tmp = ""
        for i in range(0, 16 - len(bin(regs[0])[2:])):
            tmp += "0"
        tmp += bin(regs[0])[2:]
        currentD = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`003B`' in new_data:
        freq = new_data['`003B`'] / 100


    # print(f"INSERT INTO regular ({params_tuple}) VALUES ({insert_symbols})", values_tuple,)
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
    
    cnx = db.create_server_connection()
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
    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    cursor.execute(f"DELETE FROM regular WHERE id={row_id}")

    cnx.commit()

    cursor.close()

    if cursor.rowcount >= 1:
        logger.info("Delete data to database table 'regular'")

    return cursor.rowcount