import abc
import json


class ReportTypes(abc.ABC):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def to_dict(self):
        return {'code': self.code, 'description': self.description}


class CustomerReports(ReportTypes):
    pass


class GoodsReports(ReportTypes):
    pass


def cst_report_list():
    return [CustomerReports('ABC', 'ABC - анализ'),
            CustomerReports('MIG', 'Миграции клиентов'),
            CustomerReports('GEO', 'Типы и география'),
            CustomerReports('GRP', 'Группы клиентов')]


def goods_report_list():
    return [GoodsReports('ABC', 'ABC - анализ'),
            GoodsReports('GRP', 'Группы товара'),
            GoodsReports('MTR', 'Товарная матрица'),
            GoodsReports('CLR', 'Миграции цветов'),
            GoodsReports('MIG', 'Миграции товаров')]


def money_report_list():
    return 'ABC,GRP,MTR,GEO'


def json_customer_report_list():
    return json.dumps([report.to_dict() for report in cst_report_list()], ensure_ascii=False)


def json_goods_report_list():
    return json.dumps([report.to_dict() for report in goods_report_list()], ensure_ascii=False)
