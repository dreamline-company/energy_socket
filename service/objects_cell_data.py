from service.enums.objects import CellAlarmTypesEnum

FLEX_DI_OBJECTS = {
    # Dictionary of objects that have unordered DI inputs
    # Type: dict[object_num, dict[cell_num, cell_data]];
    # The `values` dict of cell_data is a dict of available alarms,
    # where the key is DI-input's serial ID and the value is Alarm type.
    18: {
        3: {
            "values": {
                1: CellAlarmTypesEnum.On,
                2: CellAlarmTypesEnum.Off,
                3: CellAlarmTypesEnum.MTZ,
                4: CellAlarmTypesEnum.AVR,
            }
        },
        5: {
            "values": {
                5: CellAlarmTypesEnum.ZNZ,
            }
        },
        7: {
            "values": {
                6: CellAlarmTypesEnum.On,
                7: CellAlarmTypesEnum.Off,
                8: CellAlarmTypesEnum.MTZ,
                9: CellAlarmTypesEnum.MTO,
                10: CellAlarmTypesEnum.APV,
            }
        },
        9: {
            "values": {
                11: CellAlarmTypesEnum.On,
                12: CellAlarmTypesEnum.Off,
                13: CellAlarmTypesEnum.MTZ,
                14: CellAlarmTypesEnum.MTO,
                15: CellAlarmTypesEnum.ZNZ,
            }
        },
        11: {
            "values": {
                16: CellAlarmTypesEnum.On,
                17: CellAlarmTypesEnum.Off,
                18: CellAlarmTypesEnum.MTZ,
                19: CellAlarmTypesEnum.MTO,
                20: CellAlarmTypesEnum.APV,
            }
        },
        13: {
            "values": {
                21: CellAlarmTypesEnum.On,
                22: CellAlarmTypesEnum.Off,
                23: CellAlarmTypesEnum.MTZ,
                24: CellAlarmTypesEnum.MTO,
                25: CellAlarmTypesEnum.APV,
            }
        },
        15: {
            "values": {
                26: CellAlarmTypesEnum.On,
                27: CellAlarmTypesEnum.Off,
                28: CellAlarmTypesEnum.MTZ,
                29: CellAlarmTypesEnum.MTO,
                30: CellAlarmTypesEnum.ZNZ,
            }
        },
        17: {
            "values": {
                31: CellAlarmTypesEnum.On,
                32: CellAlarmTypesEnum.Off,
                33: CellAlarmTypesEnum.MTZ,
                34: CellAlarmTypesEnum.MTO,
                35: CellAlarmTypesEnum.ZNZ,
            }
        },
        20: {
            "values": {
                36: CellAlarmTypesEnum.On,
                37: CellAlarmTypesEnum.Off,
                38: CellAlarmTypesEnum.MTZ,
                39: CellAlarmTypesEnum.AVR,
            }
        },
        18: {
            "values": {
                40: CellAlarmTypesEnum.On,
                41: CellAlarmTypesEnum.Off,
                42: CellAlarmTypesEnum.MTZ,
                43: CellAlarmTypesEnum.MTO,
            }
        },
        16: {
            "values": {
                44: CellAlarmTypesEnum.On,
                45: CellAlarmTypesEnum.Off,
                46: CellAlarmTypesEnum.MTZ,
                47: CellAlarmTypesEnum.MTO,
                48: CellAlarmTypesEnum.ZNZ,
            }
        },
        14: {
            "values": {
                49: CellAlarmTypesEnum.On,
                50: CellAlarmTypesEnum.Off,
                51: CellAlarmTypesEnum.MTZ,
                52: CellAlarmTypesEnum.MTO,
            }
        },
        12: {
            "values": {
                53: CellAlarmTypesEnum.On,
                54: CellAlarmTypesEnum.Off,
                55: CellAlarmTypesEnum.MTZ,
                56: CellAlarmTypesEnum.MTO,
                57: CellAlarmTypesEnum.APV,
            }
        },
        10: {  # Can't read 31 and 32 values from DI
            "values": {
                58: CellAlarmTypesEnum.On,
                59: CellAlarmTypesEnum.Off,
                60: CellAlarmTypesEnum.MTZ,
            }
        },
        8: {
            "values": {
                61: CellAlarmTypesEnum.On,
                62: CellAlarmTypesEnum.Off,
                63: CellAlarmTypesEnum.MTZ,
                64: CellAlarmTypesEnum.MTO,
                65: CellAlarmTypesEnum.APV,
            }
        },
        6: {
            "values": {
                66: CellAlarmTypesEnum.ZNZ,
            }
        },
        4: {
            "values": {
                67: CellAlarmTypesEnum.On,
                68: CellAlarmTypesEnum.Off,
                69: CellAlarmTypesEnum.MTZ,
                70: CellAlarmTypesEnum.AVR,
            }
        },
    },
    20: {
        11: {
            "values": {
                1: CellAlarmTypesEnum.On,
                2: CellAlarmTypesEnum.Off,
                3: CellAlarmTypesEnum.MTZ,
                4: CellAlarmTypesEnum.MTO,
            }
        },
        9: {
            "values": {
                5: CellAlarmTypesEnum.On,
                6: CellAlarmTypesEnum.Off,
                7: CellAlarmTypesEnum.MTZ,
                8: CellAlarmTypesEnum.MTO,
            }
        },
        7: {
            "values": {
                9: CellAlarmTypesEnum.On,
                10: CellAlarmTypesEnum.Off,
                11: CellAlarmTypesEnum.MTZ,
                12: CellAlarmTypesEnum.MTO,
            }
        },
        5: {
            "values": {
                13: CellAlarmTypesEnum.ZMN,
            }
        },
        3: {
            "values": {
                14: CellAlarmTypesEnum.On,
                15: CellAlarmTypesEnum.Off,
                16: CellAlarmTypesEnum.MTZ,
                17: CellAlarmTypesEnum.AVR,
            }
        },
        1: {
            "values": {
                18: CellAlarmTypesEnum.On,
                19: CellAlarmTypesEnum.Off,
                20: CellAlarmTypesEnum.MTZ,
                21: CellAlarmTypesEnum.AVR,
            }
        },
        4: {
            "values": {
                22: CellAlarmTypesEnum.On,
                23: CellAlarmTypesEnum.Off,
                24: CellAlarmTypesEnum.MTZ,
                25: CellAlarmTypesEnum.AVR,
            }
        },
        6: {
            "values": {
                26: CellAlarmTypesEnum.ZMN,
            }
        },
        8: {
            "values": {
                27: CellAlarmTypesEnum.On,
                28: CellAlarmTypesEnum.Off,
                29: CellAlarmTypesEnum.MTZ,
                30: CellAlarmTypesEnum.AVR,
            }
        },
        10: {  # can't read 31 and 32 DI ports
            "values": {
                31: CellAlarmTypesEnum.MTZ,
                32: CellAlarmTypesEnum.MTO,
            }
        },
        12: {
            "values": {
                33: CellAlarmTypesEnum.On,
                34: CellAlarmTypesEnum.Off,
                35: CellAlarmTypesEnum.MTZ,
                36: CellAlarmTypesEnum.MTO,
            }
        },
    },
    21: {
        14: {
            "values": {
                1: CellAlarmTypesEnum.On,
                2: CellAlarmTypesEnum.Off,
                3: CellAlarmTypesEnum.MTZ,
                4: CellAlarmTypesEnum.MTO,
            }
        },
        12: {
            "values": {
                5: CellAlarmTypesEnum.On,
                6: CellAlarmTypesEnum.Off,
                7: CellAlarmTypesEnum.MTZ,
                8: CellAlarmTypesEnum.MTO,
                9: CellAlarmTypesEnum.ZMN,
            }
        },
        10: {
            "values": {
                10: CellAlarmTypesEnum.On,
                11: CellAlarmTypesEnum.Off,
                12: CellAlarmTypesEnum.MTZ,
                13: CellAlarmTypesEnum.MTO,
            }
        },
        8: {
            "values": {
                14: CellAlarmTypesEnum.On,
                15: CellAlarmTypesEnum.Off,
                16: CellAlarmTypesEnum.MTZ,
                17: CellAlarmTypesEnum.MTO,
            }
        },
        6: {
            "values": {
                18: CellAlarmTypesEnum.ZMN,
            }
        },
        4: {
            "values": {
                19: CellAlarmTypesEnum.On,
                20: CellAlarmTypesEnum.Off,
                21: CellAlarmTypesEnum.MTZ,
                22: CellAlarmTypesEnum.AVR,
            }
        },
        2: {
            "values": {
                23: CellAlarmTypesEnum.On,
                24: CellAlarmTypesEnum.Off,
                25: CellAlarmTypesEnum.MTZ,
                26: CellAlarmTypesEnum.AVR,
            }
        },
        3: {
            "values": {
                27: CellAlarmTypesEnum.On,
                28: CellAlarmTypesEnum.Off,
                29: CellAlarmTypesEnum.MTZ,
                30: CellAlarmTypesEnum.AVR,
            }
        },
        5: {
            "values": {
                46: CellAlarmTypesEnum.ZMN,
            }
        },
        7: {
            "values": {
                47: CellAlarmTypesEnum.On,
                31: CellAlarmTypesEnum.Off,
                32: CellAlarmTypesEnum.MTZ,
                33: CellAlarmTypesEnum.MTO,
            }
        },
        13: {
            "values": {
                34: CellAlarmTypesEnum.On,
                35: CellAlarmTypesEnum.Off,
                36: CellAlarmTypesEnum.MTZ,
                37: CellAlarmTypesEnum.MTO,
            }
        },
        9: {
            "values": {
                38: CellAlarmTypesEnum.On,
                39: CellAlarmTypesEnum.Off,
                40: CellAlarmTypesEnum.MTZ,
                41: CellAlarmTypesEnum.MTO,
            }
        },
        11: {
            "values": {
                42: CellAlarmTypesEnum.On,
                43: CellAlarmTypesEnum.Off,
                44: CellAlarmTypesEnum.MTZ,
                45: CellAlarmTypesEnum.MTO,
            }
        },
    },
    22: {
        11: {
            "values": {
                1: CellAlarmTypesEnum.On,
                2: CellAlarmTypesEnum.Off,
                3: CellAlarmTypesEnum.MTZ,
                4: CellAlarmTypesEnum.MTO,
            }
        },
        9: {
            "values": {
                5: CellAlarmTypesEnum.On,
                6: CellAlarmTypesEnum.Off,
                7: CellAlarmTypesEnum.MTZ,
                8: CellAlarmTypesEnum.MTO,
            }
        },
        7: {
            "values": {
                9: CellAlarmTypesEnum.On,
                10: CellAlarmTypesEnum.Off,
                11: CellAlarmTypesEnum.MTZ,
                12: CellAlarmTypesEnum.MTO,
            }
        },
        5: {
            "values": {
                13: CellAlarmTypesEnum.ZMN,
            }
        },
        3: {
            "values": {
                14: CellAlarmTypesEnum.On,
                15: CellAlarmTypesEnum.Off,
                16: CellAlarmTypesEnum.MTZ,
                17: CellAlarmTypesEnum.AVR,
            }
        },
        1: {
            "values": {
                18: CellAlarmTypesEnum.On,
                19: CellAlarmTypesEnum.Off,
                20: CellAlarmTypesEnum.MTZ,
                21: CellAlarmTypesEnum.AVR,
            }
        },
        4: {
            "values": {
                22: CellAlarmTypesEnum.On,
                23: CellAlarmTypesEnum.Off,
                24: CellAlarmTypesEnum.MTZ,
                25: CellAlarmTypesEnum.AVR,
            }
        },
        6: {
            "values": {
                26: CellAlarmTypesEnum.ZMN,
            }
        },
        8: {
            "values": {
                27: CellAlarmTypesEnum.On,
                28: CellAlarmTypesEnum.Off,
                29: CellAlarmTypesEnum.MTZ,
                30: CellAlarmTypesEnum.AVR,
            }
        },
        10: {  # can't read 31 and 32 DI ports
            "values": {
                31: CellAlarmTypesEnum.MTZ,
                32: CellAlarmTypesEnum.MTO,
            }
        },
        12: {
            "values": {
                33: CellAlarmTypesEnum.On,
                34: CellAlarmTypesEnum.Off,
                35: CellAlarmTypesEnum.MTZ,
                36: CellAlarmTypesEnum.MTO,
            }
        },
    },
    23: {
        22: {
            "values": {
                2: CellAlarmTypesEnum.DugZ,
                3: CellAlarmTypesEnum.Cut_Off,
                4: CellAlarmTypesEnum.MTZ,
                5: CellAlarmTypesEnum.Off,
            }
        },
        20: {
            "values": {
                6: CellAlarmTypesEnum.Off,
                7: CellAlarmTypesEnum.Cut_Off,
                8: CellAlarmTypesEnum.GroundOnLine,
                9: CellAlarmTypesEnum.DugZ,
                10: CellAlarmTypesEnum.MTZ,
            }
        },
        18: {
            "values": {
                11: CellAlarmTypesEnum.Off,
                12: CellAlarmTypesEnum.MTZ,
                13: CellAlarmTypesEnum.Cut_Off,
                14: CellAlarmTypesEnum.DugZ,
            }
        },
        16: {
            "values": {
                16: CellAlarmTypesEnum.Off,
                17: CellAlarmTypesEnum.Cut_Off,
                18: CellAlarmTypesEnum.GROUND,
                19: CellAlarmTypesEnum.MTZ,
            }
        },
        14: {
            "values": {
                22: CellAlarmTypesEnum.MaxProtection,
                23: CellAlarmTypesEnum.AVR,
                25: CellAlarmTypesEnum.Off,
            }
        },
        10: {
            "values": {
                26: CellAlarmTypesEnum.Off,
                27: CellAlarmTypesEnum.MaxProtection,
                28: CellAlarmTypesEnum.Cut_Off,
                29: CellAlarmTypesEnum.DugZ,
                30: CellAlarmTypesEnum.APV,
            }
        },
        8: {
            "values": {
                31: CellAlarmTypesEnum.Cut_Off,
                32: CellAlarmTypesEnum.DugZ
            }
        },
        6: {
            "values": {
                34: CellAlarmTypesEnum.Off,
                35: CellAlarmTypesEnum.MaxProtection,
                36: CellAlarmTypesEnum.Cut_Off,
                37: CellAlarmTypesEnum.DugZ,
                38: CellAlarmTypesEnum.APV,
            }
        },
        3: {
            "values": {
                40: CellAlarmTypesEnum.MaxProtection,
                41: CellAlarmTypesEnum.AVR,
                43: CellAlarmTypesEnum.Off,
            }
        },
        5: {
            "values": {
                44: CellAlarmTypesEnum.Off,
                45: CellAlarmTypesEnum.MaxProtection,
                46: CellAlarmTypesEnum.Cut_Off,
                47: CellAlarmTypesEnum.DugZ,
                48: CellAlarmTypesEnum.APV,
            }
        },
        7: {
            "values": {
                50: CellAlarmTypesEnum.Cut_Off,
                51: CellAlarmTypesEnum.MaxProtection,
                52: CellAlarmTypesEnum.GROUND,
                53: CellAlarmTypesEnum.Off,
            }
        },
        9: {
            "values": {
                54: CellAlarmTypesEnum.Off,
                55: CellAlarmTypesEnum.MaxProtection,
                56: CellAlarmTypesEnum.Cut_Off,
                57: CellAlarmTypesEnum.DugZ,
                58: CellAlarmTypesEnum.APV,
            }
        },
        13: {
            "values": {
                60: CellAlarmTypesEnum.MaxProtection,
                61: CellAlarmTypesEnum.Off,
            }
        },
        15: {
            "values": {
                63: CellAlarmTypesEnum.MaxProtection,
                64: CellAlarmTypesEnum.Cut_Off,
                65: CellAlarmTypesEnum.DugZ,
                66: CellAlarmTypesEnum.Off,
            }
        },
        17: {
            "values": {
                68: CellAlarmTypesEnum.MTZ,
                69: CellAlarmTypesEnum.Cut_Off,
                70: CellAlarmTypesEnum.DugZ,
                71: CellAlarmTypesEnum.Off,
            }
        },
        19: {
            "values": {
                72: CellAlarmTypesEnum.On,
                73: CellAlarmTypesEnum.MTZ,
                74: CellAlarmTypesEnum.Cut_Off,
                75: CellAlarmTypesEnum.DugZ,
                76: CellAlarmTypesEnum.GroundOnLine,
            }
        },
        21: {
            "values": {
                77: CellAlarmTypesEnum.On,
                78: CellAlarmTypesEnum.MTZ,
                79: CellAlarmTypesEnum.Cut_Off,
                80: CellAlarmTypesEnum.DugZ,
            }
        },
    },
    24: {
        12: {
            "values": {
                1: CellAlarmTypesEnum.DugZ,
            }
        },
        10: {
            "values": {
                6: CellAlarmTypesEnum.GroundProtection,
            }
        },
        8: {
            "values": {
                11: CellAlarmTypesEnum.DugZ,
                12: CellAlarmTypesEnum.AvarOtkl,
            }
        },
        6: {
            "values": {
                16: CellAlarmTypesEnum.DugZ,
                17: CellAlarmTypesEnum.AvarOtkl,
            }
        },
        4: {
            "values": {
                21: CellAlarmTypesEnum.DugZ,
                22: CellAlarmTypesEnum.AvarOtkl,
            }
        },
        11: {
            "values": {
                26: CellAlarmTypesEnum.DugZ,
                27: CellAlarmTypesEnum.AvarOtkl,
            }
        },
        9: {
            "values": {}
        },
        7: {
            "values": {
                34: CellAlarmTypesEnum.DugZ,
                35: CellAlarmTypesEnum.AvarOtkl,
            }
        },
        5: {
            "values": {
                39: CellAlarmTypesEnum.DugZ,
                40: CellAlarmTypesEnum.AvarOtkl,
            }
        },
        3: {
            "values": {
                44: CellAlarmTypesEnum.GroundProtection,
            }
        },
        1: {
            "values": {
                49: CellAlarmTypesEnum.MaxProtection,
                50: CellAlarmTypesEnum.DugZ,
            }
        },
    },
    30: {
        12: {
            "values": {
                1: CellAlarmTypesEnum.On,
                2: CellAlarmTypesEnum.Off,
                3: CellAlarmTypesEnum.MTZ,
                4: CellAlarmTypesEnum.Cut_Off,
                5: CellAlarmTypesEnum.DugZ,
            }
        },
        10: {
            "values": {
                6: CellAlarmTypesEnum.On,
                7: CellAlarmTypesEnum.Off,
                8: CellAlarmTypesEnum.MTZ,
                9: CellAlarmTypesEnum.Cut_Off,
                10: CellAlarmTypesEnum.DugZ,
            }
        },
        8: {
            "values": {
                11: CellAlarmTypesEnum.On,
                12: CellAlarmTypesEnum.Off,
                13: CellAlarmTypesEnum.MTZ,
                14: CellAlarmTypesEnum.Cut_Off,
                15: CellAlarmTypesEnum.DugZ,
            }
        },
        6: {
            "values": {
                16: CellAlarmTypesEnum.GROUND,
            }
        },
        4: {
            "values": {
                17: CellAlarmTypesEnum.On,
                18: CellAlarmTypesEnum.Off,
                19: CellAlarmTypesEnum.AVR,
                20: CellAlarmTypesEnum.MTZ_boost,
                21: CellAlarmTypesEnum.ZFZ,
            }
        },
        1: {
            "values": {
                22: CellAlarmTypesEnum.On,
                23: CellAlarmTypesEnum.Off,
                24: CellAlarmTypesEnum.AVR,
                25: CellAlarmTypesEnum.ZFZ_sec_1,
                26: CellAlarmTypesEnum.ZFZ_sec_2,
            }
        },
        3: {
            "values": {
                27: CellAlarmTypesEnum.On,
                28: CellAlarmTypesEnum.Off,
                29: CellAlarmTypesEnum.AVR,
                30: CellAlarmTypesEnum.MTZ_boost,
            }
        },
        7: {
            "values": {
                31: CellAlarmTypesEnum.On,
                32: CellAlarmTypesEnum.Off,
                33: CellAlarmTypesEnum.MTZ,
                34: CellAlarmTypesEnum.Cut_Off,
                35: CellAlarmTypesEnum.DugZ,
            }
        },
        9: {
            "values": {
                36: CellAlarmTypesEnum.On,
                37: CellAlarmTypesEnum.Off,
                38: CellAlarmTypesEnum.MTZ,
                39: CellAlarmTypesEnum.Cut_Off,
                40: CellAlarmTypesEnum.DugZ,
            }
        },
        11: {
            "values": {
                41: CellAlarmTypesEnum.On,
                42: CellAlarmTypesEnum.Off,
                43: CellAlarmTypesEnum.MTZ,
                44: CellAlarmTypesEnum.Cut_Off,
                45: CellAlarmTypesEnum.DugZ,
            }
        },
    },
}

COUNTER_ORDER = {
    23: {
        1: 22,
        2: 20,
        3: 18,
        4: 16,
        5: 14,
        6: 10,
        7: 8,
        8: 6,
        9: 5,
        10: 7,
        11: 9,
        12: 13,
        13: 15,
        14: 17,
        15: 19,
        16: 21
    }
}
