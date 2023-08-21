"""
db_var
"""
comman_var = ["id", "obj_num", "obj_name", "dt", "dt_0"]

comman_var_param = [
    "INT AUTO_INCREMENT PRIMARY KEY",
    "int NOT NULL",
    "VARCHAR(64) NOT NULL",
    "datetime NOT NULL",
    "datetime NOT NULL",
]

general_var = ["VP", "t_air", "t_cpu", "stat", "reset"]

general_var_param = ["FLOAT NOT NULL" for i in range(len(general_var))]

emergency_var = ["cell_" + str(i) for i in range(1, 25)]

emergency_var_param = ["INT" for i in range(len(emergency_var))]

regular_var = ["cell_number"] + [
    "AB" + str(bytes.hex((i).to_bytes(1, "big"))) for i in [16, 17, 18, 19, 20]
]
regular_var_param = ["INT" for i in range(len(regular_var))]

state_name = ["file_send", "reset", "set_time", "timezone"]

FILE_SEND_STATE_ID = 0
RESET_STATE_ID = 1
SET_TIME_STATE_ID = 2
