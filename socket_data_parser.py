"""
socket_data_parser
"""
from datetime import datetime, timezone, timedelta

START_CHARACTER = 60
END_CHARACTER = 62
DIVIDER_FOR_FLOAT_VALUES = 10.0

REGULAR_PACKET_TYPE = 1
EMERGENCY_PACKET_TYPE = 2
CMD_PACKET_TYPE = 3

LAST_INDEX = -1

def is_packet_valid(received_data):
    """
    Возвращает true, если полученные данные имеют допустимый формат.
    - начинаеться с '<'
    - заканчиваться на '>'
    - длина меньше MAX_LEN_PACKET
    """
    # проверяем начальный и конечный символ
    is_start_and_end_symbol = (
        received_data[0] == START_CHARACTER
        and received_data[LAST_INDEX] == END_CHARACTER
    )
    # проверяем правильность типа пакета
    is_valid_type_packet = received_data[2] - ord("0") in [
        REGULAR_PACKET_TYPE,
        EMERGENCY_PACKET_TYPE,
        CMD_PACKET_TYPE,
    ]

    is_valid_length = True

    # на основе всех критериев возвращем ответ
    return is_start_and_end_symbol and is_valid_type_packet and is_valid_length


def parse_regular_registers(base_data, main_data):
    """
    Функция возвращает массив кортежей состоящих из номера ячейки, номера регистра, значения регистра
    """
    data = []
    for cell in main_data:
        key_val = cell.split(b"|")
        # получаем номер ячейки
        cell_number = int(key_val[0].decode())
        # регистры разделинны символом ';' делим по этому символу
        registers = key_val[1].split(b";")[:LAST_INDEX]
        # logger.info(registers)
        register_data = {}
        register_data.update(base_data)
        register_data.update({"cell_number": cell_number})
        for register in registers:
            key_val_reg = register.split(b":")
            # номер регистра
            register_num = '`' + key_val_reg[0].decode().upper() + '`'
            # значение регистра
            register_val = int(key_val_reg[1].decode())
            # собираем кортеж из номера ячейки, номера регистра, значения регистра
            register_data.update({register_num: register_val})
        data.append(register_data)
    return data


def parse_general_data(base_data, received_data):
    """
    Функция возвращает кортеже состоящий из значений температуры,
    напряжения, состояний модулей, количество перезагрузок
    """

    # между послденими символами '{' и '}' находиться общая
    # информация с контроллера, вырезаем данный промежуток

    general_data_r = received_data[
        received_data.rindex(ord("{")) + 1 : received_data.rindex(ord("}"))
    ]

    # общая информация разделинна символом ',' делим по этому символу
    general_data_r = general_data_r.split(b",")[:LAST_INDEX]
    general_data = {}

    general_data.update(base_data)

    temp_map = {}
    for data_entry in general_data_r:
        key_val = data_entry.split(b":")
        # собираем кортеж из значений
        temp_map[key_val[0].decode()] = key_val[1].decode()

    general_data.update(temp_map)

    return general_data


def parse_emergency_data(base_data, main_data):
    """
    Функция возвращает кортеже состоящий из номера ячейки, значения ячейки
    """
    data = {}
    data.update(base_data)
    for index, cell in enumerate(main_data[:-1], 1):
        print(cell.decode().split(":"))
        s = cell.decode().split(":")
        data["c" + s[0]] = int(s[1])
    return data


def parse_socket_data(received_data):
    """
    Функция возвращает кортеж из тип пакета (packet_type) и спарсенных данных (data)
    """

    # нужно объединить два байта для получение номера объекта (индексы 1 и 2)
    object_number = received_data[1] - ord("0")
    # байт под индексов 3 тип пакета
    packet_type = received_data[2] - ord("0")
    # вырезаем данные с индекса 4 до символа '{' между данным промежутке находиться время с контроллера
    datetime_from_ctr = datetime.fromtimestamp(
        int(str(received_data[3 : received_data.index(ord("{"))].decode()))
    )
    # между символами '{' и '}' находиться основаная информация с контроллера, вырезаем данный промежуток
    main_data = received_data[
        received_data.index(ord("{")) + 1 : received_data.index(ord("}"))
    ]
    # данные разделинны символом ',' делим по этому символу
    main_data = main_data.split(b",")[:LAST_INDEX]

    data = ()

    base_data = {
        "obj_num": object_number,
        "dt": datetime_from_ctr,
    }

    # парсим регулярный пакет который состоит из регулярных регистров и общей информацией
    if packet_type == REGULAR_PACKET_TYPE:
        data = parse_regular_registers(base_data, main_data)
        if len(data) == 0:
            data.append(base_data)
        data.append(parse_general_data(base_data, received_data))
    # парсим аварийный пакет который состоит из номера ячейки, значения ячейки
    elif packet_type == EMERGENCY_PACKET_TYPE:
        main_data = received_data[
            received_data.index(ord("{")) + 1 : received_data.rindex(ord("}"))
        ].split(b",")
        data = parse_emergency_data(base_data, main_data)
    return packet_type, object_number, datetime_from_ctr, data
