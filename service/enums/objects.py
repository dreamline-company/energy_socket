from enum import Enum


class ObjectTypeEnum(Enum):
    Micom = "Micom"
    Di = "Di"


class CellAlarmTypesEnum(Enum):
    On = "Вкл"
    Off = "Откл"
    MTZ = "МТ3"
    AVR = "АВР"
    ZNZ = "ЗНЗ"
    MTO = "МТО"
    APV = "АПВ"
    ZMN = "ЗМН"
    DIFF = "Дифференциальная защита"
    GAS = "Газовая защита трансформатора"
    GROUND = "Земля в сети"
    DugZ = "Дуговая з."
    GroundProtection = "Земля з."
    GroundOnLine = "Земля на линии"
    AvarOtkl = "Аварийное откл."
    MaxProtection = "Макс з."
    Cut_Off = "Отсечка"
    MTZ_boost = "Ускорение МТЗ"
    ZFZ = "ЗФЗ"
    ZFZ_sec_1 = "ЗФЗ 1 сек."
    ZFZ_sec_2 = "ЗФЗ 2 сек."
    FZ = "ФЗ"
    Work_Permit = "Разрешение работы ВВ"






