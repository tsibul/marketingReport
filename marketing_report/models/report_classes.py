import abc
import json

from marketing_report.service_functions.reprt_functions.abc_report import *
from marketing_report.service_functions.reprt_functions.migration_report import *


class ReportType(abc.ABC):
    def __init__(self, code, description, report_function):
        self.code = code
        self.description = description
        self.report_function = report_function

    def to_dict(self):
        return {'code': self.code, 'description': self.description}


class CustomerReport(ReportType):
    pass


class GoodsReport(ReportType):
    pass


def cst_report_list():
    return [CustomerReport('ABC', 'ABC - анализ', cst_abc),
            CustomerReport('MIG', 'Миграции клиентов', cst_migrations),
            CustomerReport('GEO', 'Типы и география', cst_geography),
            CustomerReport('GRP', 'Группы клиентов', cst_groups)]


def goods_report_list():
    return [GoodsReport('ABC', 'ABC - анализ', goods_abc),
            GoodsReport('GRP', 'Группы товара', goods_groups),
            GoodsReport('MTR', 'Товарная матрица', goods_matrix),
            GoodsReport('CLR', 'Миграции цветов', goods_color),
            GoodsReport('MIG', 'Миграции товаров', goods_migrations)]


def money_report_list():
    return 'ABC,GRP,MTR,GEO'


def json_customer_report_list():
    return json.dumps([report.to_dict() for report in cst_report_list()], ensure_ascii=False)


def json_goods_report_list():
    return json.dumps([report.to_dict() for report in goods_report_list()], ensure_ascii=False)
