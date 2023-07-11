"""
HI e
"""
comman_var = [
    "id",
    "object_number",
    "object_name",
    "timestamp_ctr",
    "timestamp"
]

comman_var_param = [
    "INT AUTO_INCREMENT PRIMARY KEY",
    "int NOT NULL",
    "VARCHAR(64) NOT NULL",
    "datetime NOT NULL",
    "datetime NOT NULL"
]

general_var = [
    "temp",
    "volt",
    "temp_cpu",
    "module_stat",
    "res_num"
]

general_var_param = [
    "FLOAT NOT NULL" for i in range(len(general_var))
]

emergency_var = [
    "cell_number",
    "cell_value"
]

emergency_var_param = [
    "INT NOT NULL" for i in range(len(emergency_var))
]

regular_var = [
    "cell_number",
    "register_number",
    "register_value"
]

regular_var_param = [
    "INT NOT NULL" for i in range(len(regular_var))
]
