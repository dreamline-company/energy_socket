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

        
    obj_num = new_data['obj_num']
    dt = new_data['dt']

    del new_data['obj_num']
    del new_data['dt']
    working = True
    cursor.execute('select oil_field, name from `emg-eme`.n_object_num where object_num={0}'.format(str(obj_num)))
    tmp_data = cursor.fetchone()
    oil_field = tmp_data[0]
    oil_field_name = tmp_data[1]

    for key in new_data.keys():
        print(key, new_data[key])
        if 'c' in key:
            cell = key.replace('c', '')
        else:
            cell = key
        if int(new_data[key]) != 0:
            working = False
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
            cursor.execute('update `emg-eme`.n_cell_matrix set working=0, alarm_1={2}, alarm_2={3}, alarm_3={4}, alarm_4={5}, alarm_5={6} where object_num={0} and cell={1}'.format(str(obj_num), cell, alarms[0], alarms[1], alarms[2], alarms[3], alarms[4]))
            cnx.commit()

            cursor.execute('select kvt_type from `emg-eme`.n_cell_matrix where object_num={0} and cell={1}'.format(str(obj_num), str(cell)))
            kvt_type = cursor.fetchone()[0]


            if kvt_type == 10:
                if alarms[0] == 1:
                    event = 'Состояние выключателя'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[1] == 1:
                    event = 'Дифференциальная защита'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[2] == 1:
                    event = 'МТЗ'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[3] == 1:
                    event = 'газовая защита трансформатора'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[4] == 1:
                    event = 'Тест'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
            else:
                if alarms[0] == 1:
                    event = 'Состояние выключателя'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[1] == 1:
                    event = 'АПВ'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[2] == 1:
                    event = 'АВР'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[3] == 1:
                    event = 'Земля в сети'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()
                if alarms[4] == 1:
                    event = 'Тест'
                    cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) ' 
                        + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                    cnx.commit()

        else:                    
            cursor.execute('update `emg-eme`.n_cell_matrix set working=1 where object_num={0} and cell={1}'.format(str(obj_num), cell))
            cnx.commit()
    
    if working:
        cursor.execute('update `emg-eme`.n_oil_fields set working=1 where oil_field="{0}"'.format(oil_field))
        cnx.commit()
    else:
        cursor.execute('update `emg-eme`.n_oil_fields set working=0 where oil_field="{0}"'.format(oil_field))
        cnx.commit()
        cursor.execute(
            f"INSERT INTO emergency ({params_tuple}) VALUES ({insert_symbols})",
            values_tuple,
        )
        cnx.commit()

    # cnx.commit()
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
