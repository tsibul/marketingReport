from django.db import models
from django.db.models import F, Sum, Count

from marketing_report.models.goods_models import Goods
from marketing_report.models.color_models import Color
from marketing_report.models.report_period import ReportPeriod


class GoodsPeriod(models.Model):
    class Meta:
        verbose_name = 'periods where was sales of goods'

    good = models.ForeignKey(Goods, on_delete=models.CASCADE, db_index=True)
    main_color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, db_index=True)
    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)
    cost_without_vat = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    price_with_vat = models.FloatField(default=0)
    sale_with_vat = models.FloatField(default=0)
    sale_without_vat = models.FloatField(default=0)
    sales_no = models.FloatField(default=0)

    def __str__(self):
        return self.good.name + " " + self.main_color.code + "" + self.main_color.name

    def __repr__(self):
        return self.good.name + " " + self.main_color.code + "" + self.main_color.name


def create_goods_period(periods, sales_transactions):
    sales_month = sales_transactions.values(
        period=F('month'),
        good_id=F('goods'),
        color_id=F('main_color')
    ).annotate(
        quantity=Sum('quantity'),
        cost_without_vat=Sum('cost_without_vat'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        sales_no=Count('id', distinct=True),
    ).order_by('month__date_begin')
    sales_quarter = sales_transactions.values(
        period=F('quarter'),
        good_id=F('goods'),
        color_id=F('main_color')
    ).annotate(
        quantity=Sum('quantity'),
        cost_without_vat=Sum('cost_without_vat'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        sales_no=Count('id', distinct=True),
    ).order_by('quarter__date_begin')
    sales_year = sales_transactions.values(
        period=F('year'),
        good_id=F('goods'),
        color_id=F('main_color')
    ).annotate(
        quantity=Sum('quantity'),
        cost_without_vat=Sum('cost_without_vat'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        sales_no=Count('id', distinct=True),
    ).order_by('year__date_begin')
    sales_period = sales_month.union(sales_quarter, sales_year)
    sales_docs = list(map(lambda item: GoodsPeriod(
        period=ReportPeriod.objects.get(id=item['period']),
        quantity=item['total_quantity'],
        sale_without_vat=item['total_sales_without_vat'],
        sale_with_vat=item['total_sales_with_vat'],
        profit=item['total_profit'],
        sales_no=item['sales_no'],
        price_with_vat= item['sale_with_vat'] / item['quantity']
    ), sales_period))
    GoodsPeriod.objects.filter(period__in=periods).delete()
    GoodsPeriod.objects.bulk_create(sales_docs)
