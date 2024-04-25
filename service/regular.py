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
        if new_data['`0030`'] == 32768 or new_data['`0031`'] == 32768:
            currentA = -1
        else:
            regs = [new_data['`0030`'], new_data['`0031`']]
            tmp = ""
            for i in range(0, 16 - len(bin(regs[0])[2:])):
                tmp += "0"
            tmp += bin(regs[0])[2:]
            currentA = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`0032`' in new_data and '`0033`' in new_data:
        if new_data['`0032`'] == 32768 or new_data['`0033`'] == 32768:
            currentB = -1
        else:
            regs = [new_data['`0032`'], new_data['`0033`']]
            tmp = ""
            for i in range(0, 16 - len(bin(regs[0])[2:])):
                tmp += "0"
            tmp += bin(regs[0])[2:]
            currentB = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`0034`' in new_data and '`0035`' in new_data:
        if new_data['`0034`'] == 32768 or new_data['`0035`'] == 32768:
            currentC = -1
        else:
            regs = [new_data['`0034`'], new_data['`0035`']]
            tmp = ""
            for i in range(0, 16 - len(bin(regs[0])[2:])):
                tmp += "0"
            tmp += bin(regs[0])[2:]
            currentC = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`0036`' in new_data and '`0037`' in new_data:
        if new_data['`0036`'] == 32768 or new_data['`0037`'] == 32768:
            currentD = -1
        else:
            regs = [new_data['`0036`'], new_data['`0037`']]
            tmp = ""
            for i in range(0, 16 - len(bin(regs[0])[2:])):
                tmp += "0"
            tmp += bin(regs[0])[2:]
            currentD = (int(bin(regs[1])[2:] + tmp, 2)) / 100

    if '`003B`' in new_data:
        if new_data['`003B`'] == 32768:
            freq = -1
        else:
            freq = new_data['`003B`'] / 100

    if '`003D`' in new_data:
        if currentA > 1000:
            if new_data['`003D`'] == 32768:
                freq = -1
            else:
                freq = new_data['`003D`'] / 100



    obj_num = new_data['obj_num']
    cell = new_data['cell_number']

    if currentA == -1 and currentB == -1 and currentC == -1 and currentD == -1 and freq == -1:
        cursor.execute('update `emg-eme`.n_cell_matrix set working=2, micom_frequency_val={2}, micom_a_val={3}, micom_b_val={4}, micom_c_val={5}, micom_reserv_val={6} where object_num={0} and cell={1}'.format(str(obj_num), cell, freq, currentA, currentB, currentC, currentD))    
    else:
        cursor.execute('update `emg-eme`.n_cell_matrix set working=1, micom_frequency_val={2}, micom_a_val={3}, micom_b_val={4}, micom_c_val={5}, micom_reserv_val={6} where object_num={0} and cell={1}'.format(str(obj_num), cell, freq, currentA, currentB, currentC, currentD))
    
    cnx.commit()


    # print(f"INSERT INTO regular ({params_tuple}) VALUES ({insert_symbols})", values_tuple,)
    cursor.execute(
        f"INSERT INTO regular ({params_tuple}) VALUES ({insert_symbols})",
        values_tuple,
    )

    cnx.commit()

    cursor.close()

    logger.info("Insert data to database table 'regular'")

    return cursor.lastrowid


def insert_ce303_counter_data(counters_params):
    """
    Insert counters data into database
    :param counters_params: list of counters parameters. Example [
        counter_id, object_id, cell, a_voltage, b_voltage, c_voltage,
        a_amperage, b_amperage, c_amperage, frequency, power
    ]
    """
    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    for counter_param in counters_params:
        if len(counter_param) >= 11:
            object_id = counter_param[1]
            cell = counter_param[2]
            a_voltage = counter_param[3]
            b_voltage = counter_param[4]
            c_voltage = counter_param[5]
            a_current = counter_param[6]
            b_current = counter_param[7]
            c_current = counter_param[8]
            frequency = counter_param[9]
            power = counter_param[10]
            cursor.execute(
                'update n_cell_matrix set working=1, counter_frequency={2}, power={3}, voltage_a={4}, voltage_b={5}, voltage_c={6}, current_a={7}, current_b={8}, current_c={9} where object_num={0} and cell={1}'.format(
                    str(object_id),
                    cell,
                    frequency,
                    power,
                    a_voltage,
                    b_voltage,
                    c_voltage,
                    a_current,
                    b_current,
                    c_current,
                )
            )

    cnx.commit()

    cursor.close()


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