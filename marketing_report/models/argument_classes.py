import abc
import json


class ArgumentType(abc.ABC):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def to_dict(self):
        return {'code': self.code, 'description': self.description}


class MoneyType(ArgumentType):
    def __init__(self, code, description, field):
        super().__init__(code, description)
        self.field = field


class TimeType(ArgumentType):
    pass


def money_argument_list():
    return [MoneyType('SalesVat', 'Продажи с НДС', 'sales_with_vat'),
            MoneyType('SalesNoVat', 'Продажи без НДС', 'sales_without_vat'),
            MoneyType('Profit', 'Прибыль', 'profit'),
            MoneyType('SalesQuantity', 'Количество продаж', 'quantity')]


def time_argument_list():
    return [TimeType('1', 'за 1 год'),
            TimeType('2', 'за 2 года'),
            TimeType('3', 'за 3 года'),
            TimeType('4', 'за 4 года'),
            TimeType('5', 'за 5 лет')]


def json_money_argument_list():
    return json.dumps([report.to_dict() for report in money_argument_list()], ensure_ascii=False)


def json_time_argument_list():
    return json.dumps([report.to_dict() for report in time_argument_list()], ensure_ascii=False)
