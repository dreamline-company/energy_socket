from enum import Enum


class CellDIValueTypes(Enum):
    On = "Вкл"
    Off = "Откл"
    MTZ = "МТ3"
    AVR = "АВР"
    ZNZ = "ЗНЗ"
    MTO = "МТО"
    APV = "АПВ"
    ZMN = "ЗМН"


objects_cells = {
    18: {
        3: {
            "len": 4,
            "values": {
                1: CellDIValueTypes.On,
                2: CellDIValueTypes.Off,
                3: CellDIValueTypes.MTZ,
                4: CellDIValueTypes.AVR,
            }
        },
        5: {
            "len": 1,
            "values": {
                5: CellDIValueTypes.ZNZ,
            }
        },
        7: {
            "len": 5,
            "values": {
                6: CellDIValueTypes.On,
                7: CellDIValueTypes.Off,
                8: CellDIValueTypes.MTZ,
                9: CellDIValueTypes.MTO,
                10: CellDIValueTypes.APV,
            }
        },
        9: {
            "len": 5,
            "values": {
                11: CellDIValueTypes.On,
                12: CellDIValueTypes.Off,
                13: CellDIValueTypes.MTZ,
                14: CellDIValueTypes.MTO,
                15: CellDIValueTypes.ZNZ,
            }
        },
        11: {
            "len": 5,
            "values": {
                16: CellDIValueTypes.On,
                17: CellDIValueTypes.Off,
                18: CellDIValueTypes.MTZ,
                19: CellDIValueTypes.MTO,
                20: CellDIValueTypes.APV,
            }
        },
        13: {
            "len": 5,
            "values": {
                21: CellDIValueTypes.On,
                22: CellDIValueTypes.Off,
                23: CellDIValueTypes.MTZ,
                24: CellDIValueTypes.MTO,
                25: CellDIValueTypes.APV,
            }
        },
        15: {
            "len": 5,
            "values": {
                26: CellDIValueTypes.On,
                27: CellDIValueTypes.Off,
                28: CellDIValueTypes.MTZ,
                29: CellDIValueTypes.MTO,
                30: CellDIValueTypes.ZNZ,
            }
        },
        17: {
            "len": 5,
            "values": {
                31: CellDIValueTypes.On,
                32: CellDIValueTypes.Off,
                33: CellDIValueTypes.MTZ,
                34: CellDIValueTypes.MTO,
                35: CellDIValueTypes.ZNZ,
            }
        },
        20: {
            "len": 4,
            "values": {
                36: CellDIValueTypes.On,
                37: CellDIValueTypes.Off,
                38: CellDIValueTypes.MTZ,
                39: CellDIValueTypes.AVR,
            }
        },
        18: {
            "len": 4,
            "values": {
                40: CellDIValueTypes.On,
                41: CellDIValueTypes.Off,
                42: CellDIValueTypes.MTZ,
                43: CellDIValueTypes.MTO,
            }
        },
        16: {
            "len": 5,
            "values": {
                44: CellDIValueTypes.On,
                45: CellDIValueTypes.Off,
                46: CellDIValueTypes.MTZ,
                47: CellDIValueTypes.MTO,
                48: CellDIValueTypes.ZNZ,
            }
        },
        14: {
            "len": 4,
            "values": {
                49: CellDIValueTypes.On,
                50: CellDIValueTypes.Off,
                51: CellDIValueTypes.MTZ,
                52: CellDIValueTypes.MTO,
            }
        },
        12: {
            "len": 5,
            "values": {
                53: CellDIValueTypes.On,
                54: CellDIValueTypes.Off,
                55: CellDIValueTypes.MTZ,
                56: CellDIValueTypes.MTO,
                57: CellDIValueTypes.APV,
            }
        },
        10: {  # Can't read 31 and 32 values from DI
            "len": 3,
            "values": {
                58: CellDIValueTypes.On,
                59: CellDIValueTypes.Off,
                60: CellDIValueTypes.MTZ,
            }
        },
        8: {
            "len": 5,
            "values": {
                61: CellDIValueTypes.On,
                62: CellDIValueTypes.Off,
                63: CellDIValueTypes.MTZ,
                64: CellDIValueTypes.MTO,
                65: CellDIValueTypes.APV,
            }
        },
        6: {
            "len": 1,
            "values": {
                66: CellDIValueTypes.ZNZ,
            }
        },
        4: {
            "len": 4,
            "values": {
                67: CellDIValueTypes.On,
                68: CellDIValueTypes.Off,
                69: CellDIValueTypes.MTZ,
                70: CellDIValueTypes.AVR,
            }
        },
    },
    20: {
        11: {
            "len": 4,
            "values": {
                1: CellDIValueTypes.On,
                2: CellDIValueTypes.Off,
                3: CellDIValueTypes.MTZ,
                4: CellDIValueTypes.MTO,
            }
        },
        9: {
            "len": 4,
            "values": {
                5: CellDIValueTypes.On,
                6: CellDIValueTypes.Off,
                7: CellDIValueTypes.MTZ,
                8: CellDIValueTypes.MTO,
            }
        },
        7: {
            "len": 4,
            "values": {
                9: CellDIValueTypes.On,
                10: CellDIValueTypes.Off,
                11: CellDIValueTypes.MTZ,
                12: CellDIValueTypes.MTO,
            }
        },
        5: {
            "len": 1,
            "values": {
                13: CellDIValueTypes.ZMN,
            }
        },
        3: {
            "len": 4,
            "values": {
                14: CellDIValueTypes.On,
                15: CellDIValueTypes.Off,
                16: CellDIValueTypes.MTZ,
                17: CellDIValueTypes.AVR,
            }
        },
        1: {
            "len": 4,
            "values": {
                18: CellDIValueTypes.On,
                19: CellDIValueTypes.Off,
                20: CellDIValueTypes.MTZ,
                21: CellDIValueTypes.AVR,
            }
        },
        4: {
            "len": 4,
            "values": {
                22: CellDIValueTypes.On,
                23: CellDIValueTypes.Off,
                24: CellDIValueTypes.MTZ,
                25: CellDIValueTypes.AVR,
            }
        },
        6: {
            "len": 1,
            "values": {
                26: CellDIValueTypes.ZMN,
            }
        },
        8: {
            "len": 4,
            "values": {
                27: CellDIValueTypes.On,
                28: CellDIValueTypes.Off,
                29: CellDIValueTypes.MTZ,
                30: CellDIValueTypes.AVR,
            }
        },
        10: {  # can't read 31 and 32 DI ports
            "len": 2,
            "values": {
                31: CellDIValueTypes.MTZ,
                32: CellDIValueTypes.MTO,
            }
        },
        12: {
            "len": 4,
            "values": {
                33: CellDIValueTypes.On,
                34: CellDIValueTypes.Off,
                35: CellDIValueTypes.MTZ,
                36: CellDIValueTypes.MTO,
            }
        },
    }
}
