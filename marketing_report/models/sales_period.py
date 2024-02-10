from django.db import models
from django.db.models import Sum

from marketing_report.models.goods_types_models import BusinessUnit
from marketing_report.models.report_period import ReportPeriod
from marketing_report.models.sales import SalesDoc


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


class SalesPeriodBusinessUnit(SalesPeriod):
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)


def create_sales_period(min_date, max_date, sales_docs):
    sales_period = sales_docs.values(
        'period'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sales_without_vat'),
        total_sales_with_vat=Sum('sales_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Sum('no_sales'),
    ).order_by('period__name', 'period__date_begin')
    sales_docs = list(map(lambda item: SalesDoc(
        period=ReportPeriod.objects.get(id=item['period']),
        total_quantity=item['total_quantity'],
        total_sales_without_vat=item['total_sales_without_vat'],
        total_sales_with_vat=item['total_sales_with_vat'],
        total_profit=item['total_profit'],
        total_no_sales=item['total_no_sales'],
        average_check=item['total_sales_with_vat'] / item['total_no_sales']
    ), sales_period))
    SalesPeriod.objects.filter(sales_doc_date__gte=min_date, sales_doc_date__lte=max_date).delete()
    SalesPeriod.objects.bulk_create(sales_docs)


def create_sales_period_business_unit(min_date, max_date, sales_docs):
    SalesPeriod.objects.filter(sales_doc_date__gte=min_date, sales_doc_date__lte=max_date).delete()
    sales_period = sales_docs.values(
        'period', 'business_unit'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales_without_vat=Sum('sales_without_vat'),
        total_sales_with_vat=Sum('sales_with_vat'),
        total_profit=Sum('profit'),
        total_no_sales=Sum('no_sales'),
    ).order_by('period__name', 'period__date_begin')
    sales_docs = list(map(lambda item: SalesDoc(
        business_unit=BusinessUnit.objects.get(id=item['business_unit']),
        period=ReportPeriod.objects.get(id=item['period']),
        total_quantity=item['total_quantity'],
        total_sales_without_vat=item['total_sales_without_vat'],
        total_sales_with_vat=item['total_sales_with_vat'],
        total_profit=item['total_profit'],
        total_no_sales=item['total_no_sales'],
        average_check=item['total_sales_with_vat'] / item['total_no_sales']
    ), sales_period))
    SalesPeriodBusinessUnit.objects.bulk_create(sales_docs)



