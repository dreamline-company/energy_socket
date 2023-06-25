main_var = [
    "id",
    "object_number",
    "object_name",
    "timestamp_ctr",
    "temperature",
    "voltage",
    "temperature_cpu",
    "voltage_cpu",
    "timestamp",
]

main_var_param = [
    "INT AUTO_INCREMENT PRIMARY KEY",
    "int NOT NULL",
    "VARCHAR(64) NOT NULL",
    "datetime NOT NULL",
    "FLOAT NOT NULL",
    "FLOAT NOT NULL",
    "FLOAT NOT NULL",
    "FLOAT NOT NULL",
    "datetime NOT NULL",
]

emergency_var = [
    "id",
    "object_number",
    "object_name",
    "timestamp_ctr",
    "cell_number",
    "cell_value",
    "timestamp",
]

emergency_var_param = [
    "INT AUTO_INCREMENT PRIMARY KEY",
    "int NOT NULL",
    "VARCHAR(64) NOT NULL",
    "datetime NOT NULL",
    "INT NOT NULL",
    "INT NOT NULL",
    "datetime NOT NULL",
]

micom_registers = [
    "0140",
    "0169",
    "0165",
    "002B",
    "0111",
    "005A",
    "0026",
    "0030",
    "0032",
    "0034",
    "0036",
]

register_data_columns = ["reg_" + register + "_data" for register in micom_registers]

register_value_columns = ["reg_" + register + "_value" for register in micom_registers]

general_var_creation = [
    data + " int, " + value + " int"
    for (data, value) in zip(register_data_columns, register_value_columns)
]

general_var = [
    data + ", " + value
    for (data, value) in zip(register_data_columns, register_value_columns)
]
