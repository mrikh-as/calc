from enum import Enum
from typing import Union
from dataclasses import dataclass, field


class Regions(Enum):
    MSK = "Город Москва"
    MO = "Московская область"
    SPB = "Город Санкт-Петербург"


@dataclass(frozen=True)
class Coeffs:
    Sob: Union[int, float] = field(
        metadata={"description": "Норма обеспеченности жилой площади на человека"}
    )
    Ksosh: Union[int, float] = field(
        metadata={"description": "Рекомендуемая обеспеченность на 1000 жителей СОШ"}
    )
    Kdou: Union[int, float] = field(
        metadata={"description": "Рекомендуемая обеспеченность на 1000 жителей ДОУ"}
    )
    Ktek_sosh: Union[int, float] = field(
        metadata={"description": "Коэффициент цены на текущую дату СОШ"}
    )
    Ktek_dou: Union[int, float] = field(
        metadata={"description": "Коэффициент цены на текущую дату ДОУ"}
    )
    Cpost_sosh: Union[int, float] = field(
        metadata={"description": "Стоимость на одно место по постановлению СОШ"}
    )
    Cpost_dou: Union[int, float] = field(
        metadata={"description": "Стоимость на одно место по постановлению ДОУ"}
    )
    Kdate_sosh: Union[int, float] = field(
        metadata={"description": "Коэффициент цены на дату постановления СОШ"}
    )
    Kdate_dou: Union[int, float] = field(
        metadata={"description": "Коэффициент цены на дату постановления ДОУ"}
    )


class _Coeffs:
    def __init__(self):
        self._coeffs = {
            Regions.MSK: Coeffs(56, 112, 63, 12.66, 12.66, 4011, 4294, 12.57, 12.57),
            Regions.MO: Coeffs(28, 135, 65, 14.61, 15.32, 2964, 2990, 11.63, 11.44),
            Regions.SPB: Coeffs(28, 120, 61, 11.14, 11.09, 2360, 2430, 7.83, 7.87),
        }

    def __get__(self, instance, owner):
        return self._coeffs

    def __getitem__(self, region: Regions):
        return self._coeffs[region]

    def __set__(self, instance, value):
        raise AttributeError("Коэффициенты доступны только для чтения")


class Calculator:
    """
    Основной класс-калькулятор.
    Нужно создать экземпляр класса, указав в параметрах
    конструктора регион из класса Regions.
    Для расчета стоимости используется метод self.calc(),
    в котором нужно указать планируемую площадь квартир.
    """

    coeffs = _Coeffs()

    def __init__(self, region: Regions):
        if not isinstance(region, Regions):
            raise TypeError(
                f"Регион должен быть одним из значений класса Region, но получен {type(region)}"
            )
        self.region = region
        self.args = self.coeffs[region]

    def calc(self, area: Union[int, float]):
        if not isinstance(area, (int, float)):
            raise TypeError(
                f"Площадь квартир должна быть int или float, но получен {type(area)}"
            )
        elif float(area) <= 0:
            raise ValueError(
                "Площадь квартир должна быть положительным числом больше нуля"
            )

        if self.region == Regions.MSK:
            Skv = area / 0.7 / 0.93
        else:
            Skv = area

        d = self.args

        Cpost_sosh = d.Cpost_sosh
        Cpost_dou = d.Cpost_dou
        Kdate_sosh = d.Kdate_sosh
        Kdate_dou = d.Kdate_dou
        Ktek_sosh = d.Ktek_sosh
        Ktek_dou = d.Ktek_dou
        Sob = d.Sob
        Ksosh = d.Ksosh
        Kdou = d.Kdou

        Csosh = (Cpost_sosh / Kdate_sosh) * Ktek_sosh
        Cdou = (Cpost_dou / Kdate_dou) * Ktek_dou
        Ctotal_sosh = (Skv / (Sob * 1000)) * Ksosh * Csosh
        Ctotal_dou = (Skv / (Sob * 1000)) * Kdou * Cdou

        return {
            "Площадь квартир": f"{area} кв.м.",
            "Количество СОШ": f"{(Skv / (Sob * 1000)) * Ksosh:.2f} штук",
            "Количество ДОУ": f"{(Skv / (Sob * 1000)) * Kdou:.2f} штук",
            "Стоимость одного места СОШ": f"{Csosh:.2f} млн. руб.",
            "Стоимость одного места ДОУ": f"{Cdou:.2f} млн. руб.",
            "Общая стоимость СОШ": f"{Ctotal_sosh:.2f} млн. руб.",
            "Общая стоимость ДОУ": f"{Ctotal_dou:.2f} млн. руб.",
            "Совокупная стоимость СОШ и ДОУ": f"{round(Ctotal_sosh + Ctotal_dou, 2)} млн. руб.",
        }


if __name__ == "__main__":
    calc = Calculator(Regions.MSK)
    result = calc.calc(1000)
    for key, value in result.items():
        print(f"{key}: {value}")
