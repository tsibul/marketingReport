from django.db import models
from django.db.models import F, Sum, Count

from marketing_report.models import BusinessUnit
from marketing_report.models.customer_group_models import CustomerGroup
from marketing_report.models.customer_models import Customer
from marketing_report.models.report_period import ReportPeriod


class CustomerPeriod(models.Model):
    class Meta:
        verbose_name = 'periods where was transactions with Client'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)

    quantity = models.IntegerField(default=0, verbose_name='количество')
    sales_without_vat = models.FloatField(default=0, null=True)
    sales_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи с НДС')
    profit = models.FloatField(default=0, null=True, verbose_name='прибыль')
    no_sales = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')
    average_check = models.FloatField(default=0, null=True, verbose_name='средний чек')

    def __str__(self):
        return self.customer.name

    def __repr__(self):
        return self.customer.name


def create_customer_period(periods, sales_docs):
    sales_month = sales_docs.values(
        period=F('month'),
        cst_id=F('customer')
    ).annotate(
        quantity=Sum('quantity'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        no_sales=Count('id', distinct=True),
    ).order_by('month__date_begin')
    sales_quarter = sales_docs.values(
        period=F('quarter'),
        cst_id=F('customer')
    ).annotate(
        quantity=Sum('quantity'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        no_sales=Count('id', distinct=True),
    ).order_by('quarter__date_begin')
    sales_year = sales_docs.values(
        period=F('year'),
        cst_id=F('customer'),
    ).annotate(
        quantity=Sum('quantity'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        no_sales=Count('id', distinct=True),
    ).order_by('year__date_begin')
    sales_period = sales_month.union(sales_quarter, sales_year)
    sales_docs = list(map(lambda item: CustomerPeriod(
        period=ReportPeriod.objects.get(id=item['period']),
        customer=Customer.objects.get(id=item['cst_id']),

        quantity=item['quantity'],
        sales_without_vat=item['sale_without_vat'],
        sales_with_vat=item['sale_with_vat'],
        profit=item['profit'],
        no_sales=item['no_sales'],
        average_check=item['sale_with_vat'] / item['no_sales']
    ), sales_period))
    CustomerPeriod.objects.filter(period__in=periods).delete()
    CustomerPeriod.objects.bulk_create(sales_docs)


class CustomerPeriodByUnit(models.Model):
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)

    quantity = models.IntegerField(default=0, verbose_name='количество')
    sales_without_vat = models.FloatField(default=0, null=True)
    sales_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи с НДС')
    profit = models.FloatField(default=0, null=True, verbose_name='прибыль')
    no_sales = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')
    average_check = models.FloatField(default=0, null=True, verbose_name='средний чек')

    def __str__(self):
        return self.customer.name + ' ' + self.business_unit.name

    def __repr__(self):
        return self.customer.name + ' ' + self.business_unit.name


def create_customer_period_business_unit(periods, sales_docs):
    sales_month = sales_docs.values(
        business_un_id=F('business_unit'),
        period=F('month'),
        cst_id=F('customer')
    ).annotate(
        quantity=Sum('quantity'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        no_sales=Count('id', distinct=True),
    ).order_by('month__date_begin')
    sales_quarter = sales_docs.values(
        business_un_id=F('business_unit'),
        period=F('quarter'),
        cst_id=F('customer')
    ).annotate(
        quantity=Sum('quantity'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        no_sales=Count('id', distinct=True),
    ).order_by('quarter__date_begin')
    sales_year = sales_docs.values(
        business_un_id=F('business_unit'),
        period=F('year'),
        cst_id=F('customer'),
    ).annotate(
        quantity=Sum('quantity'),
        sale_without_vat=Sum('sale_without_vat'),
        sale_with_vat=Sum('sale_with_vat'),
        profit=Sum('profit'),
        no_sales=Count('id', distinct=True),
    ).order_by('year__date_begin')
    sales_period = sales_month.union(sales_quarter, sales_year)
    sales_docs = list(map(lambda item: CustomerPeriodByUnit(
        business_unit=BusinessUnit.objects.get(id=item['business_un_id']),
        period=ReportPeriod.objects.get(id=item['period']),
        customer=Customer.objects.get(id=item['cst_id']),

        quantity=item['quantity'],
        sales_without_vat=item['sale_without_vat'],
        sales_with_vat=item['sale_with_vat'],
        profit=item['profit'],
        no_sales=item['no_sales'],
        average_check=item['sale_with_vat'] / item['no_sales']
    ), sales_period))
    CustomerPeriodByUnit.objects.filter(period__in=periods).delete()
    CustomerPeriodByUnit.objects.bulk_create(sales_docs)
