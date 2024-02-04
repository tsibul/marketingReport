import abc
import json


class ArgumentType(abc.ABC):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def to_dict(self):
        return {'code': self.code, 'description': self.description}


class MoneyType(ArgumentType):
    pass


class TimeType(ArgumentType):
    pass


def money_argument_list():
    return [MoneyType('SalesVat', 'Продажи с НДС'),
            MoneyType('SalesNoVat', 'Продажи без НДС'),
            MoneyType('Profit', 'Прибыль'),
            MoneyType('SalesQuantity', 'Количество продаж')]


def time_argument_list():
    return [TimeType('1', '1 год'),
            TimeType('2', '2 года'),
            TimeType('3', '3 года'),
            TimeType('4', '4 года'),
            TimeType('5', '5 лет')]


def json_money_argument_list():
    return json.dumps([report.to_dict() for report in money_argument_list()], ensure_ascii=False)


def json_time_argument_list():
    return json.dumps([report.to_dict() for report in time_argument_list()], ensure_ascii=False)
