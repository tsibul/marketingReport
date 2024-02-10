from django.db import models
from django.db.models import Sum, F, Count

from marketing_report.models.goods_types_models import BusinessUnit
from marketing_report.models.report_period import ReportPeriod


class SalesPeriod(models.Model):
    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE)

    total_quantity = models.IntegerField(default=0, verbose_name='количество')
    total_sales_without_vat = models.FloatField(default=0, null=True)
    total_sales_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи с НДС')
    total_profit = models.FloatField(default=0, null=True, verbose_name='прибыль')
    total_no_sales = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')
    average_check = models.FloatField(default=0, null=True, verbose_name='средний чек')

    def __str__(self):
        return self.period.name

    def __repr__(self):
        return self.period.name


def create_sales_period(periods, sales_docs):
    sales_month = sales_docs.values(
        period=F('month')
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sale_without_vat'),
        total_sales_with_vat=Sum('sale_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Count('id', distinct=True),
    ).order_by('month__date_begin')
    sales_quarter = sales_docs.values(
        period=F('quarter')
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sale_without_vat'),
        total_sales_with_vat=Sum('sale_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Count('id', distinct=True),
    ).order_by('quarter__date_begin')
    sales_year = sales_docs.values(
        period=F('year')
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sale_without_vat'),
        total_sales_with_vat=Sum('sale_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Count('id', distinct=True),
    ).order_by('year__date_begin')
    sales_period = sales_month.union(sales_quarter, sales_year)
    sales_docs = list(map(lambda item: SalesPeriod(
        period=ReportPeriod.objects.get(id=item['period']),
        total_quantity=item['total_quantity'],
        total_sales_without_vat=item['total_sales_without_vat'],
        total_sales_with_vat=item['total_sales_with_vat'],
        total_profit=item['total_profit'],
        total_no_sales=item['total_no_sales'],
        average_check=item['total_sales_with_vat'] / item['total_no_sales']
    ), sales_period))
    SalesPeriod.objects.filter(period__in=periods).delete()
    SalesPeriod.objects.bulk_create(sales_docs)


class SalesPeriodBusinessUnit(models.Model):
    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)

    total_quantity = models.IntegerField(default=0, verbose_name='количество')
    total_sales_without_vat = models.FloatField(default=0, null=True)
    total_sales_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи с НДС')
    total_profit = models.FloatField(default=0, null=True, verbose_name='прибыль')
    total_no_sales = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')
    average_check = models.FloatField(default=0, null=True, verbose_name='средний чек')

    def __str__(self):
        return self.period.name + ' - ' + self.business_unit.name

    def __repr__(self):
        return self.period.name + ' - ' + self.business_unit.name


def create_sales_period_business_unit(periods, sales_docs):
    sales_month = sales_docs.values(
        period=F('month'),
        business_un=F('business_unit')
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sale_without_vat'),
        total_sales_with_vat=Sum('sale_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Count('id', distinct=True),
    ).order_by('month__date_begin')
    sales_quarter = sales_docs.values(
        period=F('quarter'),
        business_un=F('business_unit')
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sale_without_vat'),
        total_sales_with_vat=Sum('sale_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Count('id', distinct=True),
    ).order_by('quarter__date_begin')
    sales_year = sales_docs.values(
        period=F('year'),
        business_un=F('business_unit')
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sale_without_vat'),
        total_sales_with_vat=Sum('sale_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Count('id', distinct=True),
    ).order_by('year__date_begin')
    sales_period = sales_month.union(sales_quarter, sales_year)
    sales_docs = list(map(lambda item: SalesPeriodBusinessUnit(
        business_unit=BusinessUnit.objects.get(id=item['business_un']),
        period=ReportPeriod.objects.get(id=item['period']),
        total_quantity=item['total_quantity'],
        total_sales_without_vat=item['total_sales_without_vat'],
        total_sales_with_vat=item['total_sales_with_vat'],
        total_profit=item['total_profit'],
        total_no_sales=item['total_no_sales'],
        average_check=item['total_sales_with_vat'] / item['total_no_sales']
    ), sales_period))
    SalesPeriodBusinessUnit.objects.filter(period__in=periods).delete()
    SalesPeriodBusinessUnit.objects.bulk_create(sales_docs)



