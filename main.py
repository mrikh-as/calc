from enum import Enum
from typing import Union


class Region(Enum):
    Moscow = "город Москва"
    MoscowObl = "Московская область"
    LenObl = "Ленинградская область"


CONSTANTS = {
    Region.Moscow: {
        "Sob": 56,
        "Ksosh": 124,
        "Kdou": 63,
        "Ktek": 12.66,
        "Cpost_sosh": 4011,
        "Cpost_dou": 4294,
        "Kdate": 12.57,
    },
    Region.MoscowObl: {
        "Sob": 28,
        "Ksosh": 135,
        "Kdou": 65,
        "Ktek_sosh": 14.61,
        "Ktek_dou": 15.32,
        "Cpost_sosh": 2964,
        "Cpost_dou": 2990,
        "Kdate_sosh": 11.63,
        "Kdate_dou": 11.44,
    },
    Region.LenObl: {
        "Sob": 33,
        "Ksosh": 110,
        "Kdou": 61,
        "Ktek": "NULL",
        "Kfirst": "NULL",
        "Cbase_sosh": 1171,
        "Cbase_dou": 1316,
        "Kper": 0.92,
        "Kper_z": 1,
        "Kreg_1": 1,
        "Kreg_2": 1,
        "Ks": 1,
        "Zdop": 1,
        "NDS": 1.2,
    },
}


def c_msc(Skv: Union[int, float], CONSTANTS: dict):
    d = CONSTANTS[Region.Moscow]
    Cpost_sosh = d["Cpost_sosh"]
    Cpost_dou = d["Cpost_dou"]
    Kdate = d["Kdate"]
    Ktek = d["Ktek"]
    Sob = d["Sob"]
    Ksosh = d["Ksosh"]
    Kdou = d["Kdou"]
    Sspp = Skv / 0.7 / 0.93
    Csosh = (Cpost_sosh / Kdate) * Ktek
    Cdou = (Cpost_dou / Kdate) * Ktek
    Ctotal_sosh = (Sspp / (Sob * 1000)) * Ksosh * Csosh
    Ctotal_dou = (Sspp / (Sob * 1000)) * Kdou * Cdou
    print(
        f"Площадь квартир: {Skv} кв.м.\nСтоимость на школы: {round(Ctotal_sosh, 2)} млн. руб.\nСтоимость на детские садики: {round(Ctotal_dou, 2)} млн. руб.\nИтоговая стоимость: {round((Ctotal_sosh+Ctotal_dou), 2)} млн. руб."
    )


def c_moscobl(Skv: Union[int, float], CONSTANTS: dict):
    d = CONSTANTS[Region.MoscowObl]
    Cpost_sosh = d["Cpost_sosh"]
    Cpost_dou = d["Cpost_dou"]
    Kdate_sosh = d["Kdate_sosh"]
    Kdate_dou = d["Kdate_dou"]
    Ktek_sosh = d["Ktek_sosh"]
    Ktek_dou = d["Ktek_dou"]
    Sob = d["Sob"]
    Ksosh = d["Ksosh"]
    Kdou = d["Kdou"]
    Csosh = (Cpost_sosh / Kdate_sosh) * Ktek_sosh
    Cdou = (Cpost_dou / Kdate_dou) * Ktek_dou
    Ctotal_sosh = (Skv / (Sob * 1000)) * Ksosh * Csosh
    Ctotal_dou = (Skv / (Sob * 1000)) * Kdou * Cdou
    print(
        f"Площадь квартир: {Skv} кв.м.\nСтоимость на школы: {round(Ctotal_sosh, 2)} млн. руб.\nСтоимость на детские садики: {round(Ctotal_dou, 2)} млн. руб.\nИтоговая стоимость: {round((Ctotal_sosh+Ctotal_dou), 2)} млн. руб."
    )


c_msc(74218, CONSTANTS)
c_moscobl(101532.4, CONSTANTS)
