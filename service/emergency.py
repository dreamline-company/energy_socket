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
    obj_num = new_data['obj_num']
    dt = new_data['dt']

    del new_data['obj_num']
    del new_data['dt']
    working = True
    cursor.execute('select oil_field from `emg-eme`.n_object_num where object_num={0}'.format(str(obj_num)))
    oil_field = cursor.fetchone()[0]

    for key in new_data.keys():
        print(key, new_data[key])
        if int(new_data[key]) != 0:
            working = False
            if 'c' in key:
                cell = key.replace('c', '')
            else:
                cell = key

            signal = "{0:b}".format(new_data[key])
            ind = 0
            print(signal)
            alarms = [0, 0, 0, 0, 0]
            for c in signal[::-1]:
                if c == '1':
                    alarms[ind] = 1
                    print('ind -- ', ind)                    
                ind += 1
            print(alarms)
            cursor.execute('update emg-eme.n_cell_matrix set working=0, alarm_1={2}, alarm_2={3}, alarm_3={4}, alarm_4={5}, alarm_5={6} where object_num={0} and cell={1}'.format(str(obj_num), cell, alarms[0], alarms[1], alarms[2], alarms[3], alarms[4]))    
            cnx.commit()

        else:                    
            cursor.execute('update emg-eme.n_cell_matrix set working=1 where object_num={0} and cell={1}'.format(str(obj_num), cell))
            cnx.commit()
    
    if working:
        cursor.execute('update emg-eme.n_oil_fields set working=1 where oil_field="{0}"'.format(oil_field))
    else:
        cursor.execute('update emg-eme.n_oil_fields set working=0 where oil_field="{0}"'.format(oil_field))

    cnx.commit()
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
