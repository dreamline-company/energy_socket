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

general_var = ["vp", "t_air", "t_cpu", "stat", "reset"]

general_var_param = ["FLOAT NOT NULL" for i in range(len(general_var))]

regular_var = ["cell_" + str(i) for i in range(1, 25)]

regular_var_param = ["INT" for i in range(len(regular_var))]

regular_var = ["cell_number"] + []
regular_var_param = ["INT" for i in range(len(regular_var))]

object_var = []
