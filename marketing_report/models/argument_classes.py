import abc
import json


class ArgumentTypes(abc.ABC):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def to_dict(self):
        return {'code': self.code, 'description': self.description}


class MoneyTypes(ArgumentTypes):
    pass


class TimeTypes(ArgumentTypes):
    pass


def money_argument_list():
    return [MoneyTypes('SalesVat', 'Продажи с НДС'),
            MoneyTypes('SalesNoVat', 'Продажи без НДС'),
            MoneyTypes('Profit', 'Прибыль'),
            MoneyTypes('SalesQuantity', 'Количество продаж')]


def time_argument_list():
    return [TimeTypes('1', '1 год'),
            TimeTypes('2', '2 года'),
            TimeTypes('3', '3 года'),
            TimeTypes('4', '4 года'),
            TimeTypes('5', '5 лет')]


def json_money_argument_list():
    return json.dumps([report.to_dict() for report in money_argument_list()], ensure_ascii=False)


def json_time_argument_list():
    return json.dumps([report.to_dict() for report in time_argument_list()], ensure_ascii=False)
