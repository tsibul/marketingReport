from django.db import models
from marketing_report.models.goods_models import Goods
from marketing_report.models.color_models import Color
from marketing_report.models.report_period import ReportPeriod


class GoodsPeriods(models.Model):

    class Meta:
        abstract = True
        verbose_name = 'periods where was sales of goods'

    good = models.ForeignKey(Goods, on_delete=models.CASCADE, db_index=True)
    main_color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, db_index=True)

    quantity = models.IntegerField(default=0)
    cost_without_vat = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    price_with_vat = models.FloatField(default=0)
    price_without_vat = models.FloatField(default=0)
    sale_with_vat = models.FloatField(default=0)
    sale_without_vat = models.FloatField(default=0)

    def set_goods_data(self, sales_imports):
        quantity = 0
        profit = 0
        buy_without_vat = 0
        sale_with_vat = 0
        sale_without_vat = 0
        for sales in sales_imports:
            quantity += sales.quantity
            sale_with_vat += sales.sale_with_vat
            sale_without_vat += sales.sale_without_vat
            buy_without_vat += sales.buy_without_vat
            profit += sales.sale_without_vat - sales.buy_without_vat
        if quantity:
            self.quantity = quantity
            self.sale_without_vat = sale_without_vat
            self.sale_with_vat = sale_with_vat
            self.profit = profit
            self.price_without_vat = self.sale_without_vat / quantity
            self.price_with_vat = self.sale_with_vat / quantity
            self.cost_without_vat = buy_without_vat / quantity


class GoodsPeriodsMonth(GoodsPeriods):

    class Meta(GoodsPeriods.Meta):
        verbose_name = 'ежемесячные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'MT'})

    def __repr__(self):
        return self.good.name + ' ' + self.period.name

    def __str__(self):
        return self.good.name + ' ' + self.period.name


class GoodsPeriodsQuarter(GoodsPeriods):

    class Meta(GoodsPeriods.Meta):
        verbose_name = 'ежеквартальные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'QT'})

    def __repr__(self):
        return self.good.name + ' ' + self.period.name

    def __str__(self):
        return self.good.name + ' ' + self.period.name


class GoodsPeriodsYear(GoodsPeriods):

    class Meta(GoodsPeriods.Meta):
        verbose_name = 'ежегодные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'YR'})

    def __repr__(self):
        return self.good.name + ' ' + self.period.name

    def __str__(self):
        return self.good.name + ' ' + self.period.name
