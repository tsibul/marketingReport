from django.db import models
from marketing_report.models.customer_group_models import CustomerGroup
from marketing_report.models.customer_models import Customer
from marketing_report.models.report_period import ReportPeriod


class CustomerPeriods(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'periods where was transactions with Client'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    group = models.ForeignKey(CustomerGroup, models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True, default=customer.name, db_index=True)
    quantity = models.IntegerField(default=0, verbose_name='количество')
    quantity_eco = models.IntegerField(default=0, verbose_name='количество эко')
    quantity_no_eco = models.IntegerField(default=0, verbose_name='количество неэко')
    sales_with_vat = models.FloatField(default=0, null=True, verbose_name='продажи с НДС')
    sales_with_vat_eco = models.FloatField(default=0, null=True, verbose_name='продажи эко с НДС')
    sales_with_vat_no_eco = models.FloatField(default=0, null=True, verbose_name='продажи неэко с НДС')
    profit = models.FloatField(default=0, null=True, verbose_name='прибыль')
    profit_eco = models.FloatField(default=0, null=True, verbose_name='прибыль эко')
    profit_no_eco = models.FloatField(default=0, null=True, verbose_name='прибыль неэко')
    no_sales = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')
    no_sales_eco = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж эко')
    no_sales_no_eco = models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж неэко')
    average_check = models.FloatField(default=0, null=True, verbose_name='средний чек')
    average_check_eco = models.FloatField(default=0, null=True, verbose_name='средний чек эко')
    average_check_no_eco = models.FloatField(default=0, null=True, verbose_name='средний чек неэко')

    def set_sales_data(self, sales_docs):
        sales_with_vat = 0
        sales_with_vat_eco = 0
        sales_with_vat_no_eco = 0
        profit = 0
        profit_eco = 0
        profit_no_eco = 0
        no_sales = 0
        no_sales_eco = 0
        no_sales_no_eco = 0
        quantity = 0
        quantity_eco = 0
        quantity_no_eco = 0
        for sales_doc in sales_docs:
            no_sales += 1
            sales_with_vat += sales_doc.total_sale_with_vat
            profit += sales_doc.total_sale_without_vat - sales_doc.total_buy_without_vat
            quantity += sales_doc.quantity
            if sales_doc.eco:
                no_sales_eco += 1
                sales_with_vat_eco += sales_doc.total_sale_with_vat
                profit_eco += sales_doc.total_sale_without_vat - sales_doc.total_buy_without_vat
                quantity_eco += sales_doc.quantity
            else:
                no_sales_no_eco += 1
                sales_with_vat_no_eco += sales_doc.total_sale_with_vat
                profit_no_eco += sales_doc.total_sale_without_vat - sales_doc.total_buy_without_vat
                quantity_no_eco += sales_doc.quantity
        self.average_check = sales_with_vat / no_sales if no_sales else 0
        self.average_check_eco = sales_with_vat_eco / no_sales_eco if no_sales_eco else 0
        self.average_check_no_eco = sales_with_vat_no_eco / no_sales_no_eco if no_sales_no_eco else 0
        self.no_sales = no_sales
        self.no_sales_eco = no_sales_eco
        self.no_sales_no_eco = no_sales_no_eco
        self.quantity = quantity
        self.quantity_eco = quantity_eco
        self.quantity_no_eco = quantity_no_eco
        self.sales_with_vat = sales_with_vat
        self.sales_with_vat_eco = sales_with_vat_eco
        self.sales_with_vat_no_eco = sales_with_vat_no_eco
        self.profit = profit
        self.profit_eco = profit_eco
        self.profit_no_eco = profit_no_eco


class CustomerPeriodsMonth(CustomerPeriods):
    class Meta(CustomerPeriods.Meta):
        verbose_name = 'ежемесячные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'MT'})

    def __repr__(self):
        return self.customer.name + ' ' + self.period.name

    def __str__(self):
        return self.customer.name + ' ' + self.period.name


class CustomerPeriodsQuarter(CustomerPeriods):
    class Meta(CustomerPeriods.Meta):
        verbose_name = 'ежевартальные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'QT'})

    def __repr__(self):
        return self.customer.name + ' ' + self.period.name

    def __str__(self):
        return self.customer.name + ' ' + self.period.name


class CustomerPeriodsYear(CustomerPeriods):
    class Meta(CustomerPeriods.Meta):
        verbose_name = 'ежегодные данные'

    period = models.ForeignKey(ReportPeriod, on_delete=models.CASCADE, limit_choices_to={'period': 'YR'})

    def __repr__(self):
        return self.name + ' ' + self.period.name

    def __str__(self):
        return self.name + ' ' + self.period.name
