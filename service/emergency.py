""" 
emergency
"""
import logging
import logging.config
import database.db as db
from service.objects_cell_data import FLEX_DI_OBJECTS, CellDIValueTypes

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


def check_for_last_emergency_data(
        cnx,
        cursor,
        event,
        cell,
        oil_field,
        obj_num,
):
    SELECT_EVENT_COUNT = 'SELECT COUNT(*) FROM `emg-eme`.n_lenta WHERE opened >= NOW() - INTERVAL 30 MINUTE AND event = "{}" AND well = {} AND oil_field = "{}" AND otvod = {}'.format(
        event,
        cell,
        oil_field,
        obj_num,
    )
    cursor.execute(SELECT_EVENT_COUNT)
    res = cursor.fetchone()
    count = res[0]
    if count > 0:
        return True
    return False


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
            signal = "{0:b}".format(new_data[key])
            ind = 0
            print(signal)
            if new_data[key] < 128:
                alarms = [0, 0, 0, 0, 0]
                for c in signal[::-1]:
                    if c == '1':
                        alarms[ind] = 1
                        print('ind -- ', ind)
                    ind += 1
                print(alarms)
                cursor.execute('update `emg-eme`.n_cell_matrix set alarm_1={2}, alarm_2={3}, alarm_3={4}, alarm_4={5}, alarm_5={6} where object_num={0} and cell={1}'.format(str(obj_num), cell, alarms[0], alarms[1], alarms[2], alarms[3], alarms[4]))
                cnx.commit()

                cursor.execute('select kvt_type from `emg-eme`.n_cell_matrix where object_num={0} and cell={1}'.format(str(obj_num), str(cell)))
                kvt_type = cursor.fetchone()[0]


                if alarms[1] == 1 or alarms[2] == 1 or alarms[3] == 1 or alarms[4] == 1:
                    working = False
                    if alarms[0] == 1:
                        cursor.execute('update `emg-eme`.n_cell_matrix set working=0, on_off=0 where object_num={0} and cell={1}'.format(str(obj_num), cell))
                        cnx.commit()
                    else:
                        cursor.execute('update `emg-eme`.n_cell_matrix set working=0, on_off=1 where object_num={0} and cell={1}'.format(str(obj_num), cell))
                        cnx.commit()
                else:
                    if alarms[0] == 1:
                        cursor.execute('update `emg-eme`.n_cell_matrix set working=1, on_off=0 where object_num={0} and cell={1}'.format(str(obj_num), cell))
                        cnx.commit()
                    else:
                        cursor.execute('update `emg-eme`.n_cell_matrix set working=1, on_off=1 where object_num={0} and cell={1}'.format(str(obj_num), cell))
                        cnx.commit()

                if kvt_type == 10:
                    if alarms[1] == 1:
                        event = 'Дифференциальная защита'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()
                    if alarms[2] == 1:
                        event = 'МТЗ'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()
                    if alarms[3] == 1:
                        event = 'Газовая защита трансформатора'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()
                    if alarms[4] == 1:
                        event = 'Тест'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()
                else:
                    if alarms[1] == 1:
                        event = 'АПВ'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()
                    if alarms[2] == 1:
                        event = 'АВР'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()
                    if alarms[3] == 1:
                        event = 'Земля в сети'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()
                    if alarms[4] == 1:
                        event = 'Тест'
                        if not check_for_last_emergency_data(
                                cnx,
                                cursor,
                                event,
                                str(cell),
                                oil_field_name,
                                str(obj_num)
                        ):
                            cursor.execute('insert into `emg-eme`.n_lenta (criticality,extraction,event,status,oil_field,well,otvod,opened) '
                                + 'values (3, "fluid", "{0}", "open", "{1}", "{2}", "{3}", now())'.format(event, oil_field_name, str(cell), str(obj_num)))
                            cnx.commit()

        else:                    
            cursor.execute('update `emg-eme`.n_cell_matrix set working=1, on_off=1, alarm_1=0, alarm_2=0, alarm_3=0, alarm_4=0, alarm_5=0 where object_num={0} and cell={1}'.format(str(obj_num), cell))
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

    cursor.close()

    logger.info("Insert data to database table 'emergency'")

    return cursor.lastrowid


def create_flex_emergency(data):
    cnx = db.create_server_connection()
    cursor = cnx.cursor()
    params_tuple = ",".join(tuple(data.keys()))
    values_tuple = tuple(data.values())
    object_num = data['obj_num']
    insert_symbols = ",".join(tuple((["%s"] * len(data.keys()))))
    if "c0" in params_tuple:
        cell_values = values_tuple[3:]
    else:
        cell_values = values_tuple[2:]
    bin_values = []
    for cell in cell_values:
        if cell >= 128:
            cell = 0
        bin_values.append(bin(cell).replace("0b", ""))

    bin_list = []
    for b in bin_values:
        old_cell = ["0", "0", "0", "0", "0"]
        reversed_bin = b[::-1]
        for i, n in enumerate(reversed_bin):
            old_cell[i] = str(n)
        bin_list.append("".join(old_cell))
    joined_list = "".join(bin_list)
    new_cell_values = []
    for cell, data in FLEX_DI_OBJECTS[object_num].items():
        reversed_cell_bin = ""
        cell_status = dict(
            working=1,
            on_off=0,
        )
        alarms = []
        for di_id, type_ in data["values"].items():
            bin_value = joined_list[di_id - 1]
            if bin_value == "1":
                if type_ == CellDIValueTypes.On:
                    cell_status["on_off"] = 1
                if type_ == CellDIValueTypes.Off:
                    cell_status["on_off"] = 0
                if type_ != CellDIValueTypes.On or type_ != CellDIValueTypes.Off:
                    alarms.append(type_.value)
            reversed_cell_bin += bin_value
        if len(alarms) >= data["max_alarms"]:
            cell_status["working"] = 0
        cell_bin = reversed_cell_bin[::-1]
        new_cell_values.append(int(cell_bin, 2))
        cursor.execute(
            'update `emg-eme`.n_cell_matrix set working={2}, on_off={3}, alarms={4} where object_num={0} and cell={1}'.format(
                str(object_num),
                cell,
                cell_status["working"],
                cell_status["on_off"],
                ", ".join(alarms),
            )
        )
        cnx.commit()

    new_values_tuple = (
        (
            values_tuple[:3] if "c0" in params_tuple else values_tuple[:2]
        ) + tuple(new_cell_values)
    )
    cursor.execute(
        f"INSERT INTO emergency ({params_tuple}) VALUES ({insert_symbols})",
        new_values_tuple,
    )
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
