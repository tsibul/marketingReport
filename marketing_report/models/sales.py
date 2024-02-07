import datetime

from django.db import models
from marketing_report.models.report_period import ReportPeriod
from marketing_report.models.customer_models import Customer
from marketing_report.models.goods_models import Goods
from marketing_report.models.color_models import Color


class SalesDoc(models.Model):

    class Meta:
        verbose_name = 'отгрузочные документы'

    sales_document = models.CharField(max_length=255)
    sales_doc_number = models.CharField(max_length=20, null=True)
    sales_doc_date = models.DateField(default=datetime.date(2000, 1, 1))
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    quantity = models.FloatField(default=0)
    total_sale_with_vat = models.FloatField(default=0)
    total_sale_without_vat = models.FloatField(default=0)
    total_buy_with_vat = models.FloatField(default=0)
    total_buy_without_vat = models.FloatField(default=0)
    order = models.CharField(max_length=100, null=True)
    good_no_error = models.BooleanField(default=True)
    eco = models.BooleanField(default=True)
    week = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='week')
    month = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='month')
    quarter = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='quarter')
    year = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='year')

    def __repr__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date)

    def __str__(self):
        return str(self.sales_doc_number) + ' от ' + str(self.sales_doc_date)

    def set_periods(self):
        month = ReportPeriod.objects.get(period='MT', date_begin__lte=self.sales_doc_date,
                                         date_end__gte=self.sales_doc_date)
        quarter = ReportPeriod.objects.get(period='QT', date_begin__lte=self.sales_doc_date,
                                           date_end__gte=self.sales_doc_date)
        year = ReportPeriod.objects.get(period='YR', date_begin__lte=self.sales_doc_date,
                                        date_end__gte=self.sales_doc_date)
        self.month = month
        self.quarter = quarter
        self.year = year


class Sales(models.Model):
    """ Frigat fields from report:
    series_id
    good_id
    good_group_id
    good_group
    good_title
    good_name
    code_1
    """

    import_date = models.DateField(default=datetime.date(2000, 1, 1))
    code = models.CharField(max_length=30)
    goods = models.ForeignKey(Goods, models.SET_NULL, null=True, db_index=True)
    color_code = models.CharField(max_length=40, null=True)
    main_color = models.CharField(max_length=12, null=True)
    color = models.ForeignKey(Color, models.SET_NULL, null=True)
    series_id = models.IntegerField(null=True)
    good_id = models.IntegerField(null=True)
    good_group_id = models.IntegerField(null=True)
    good_group = models.CharField(max_length=255, null=True)
    good_title = models.CharField(max_length=255, null=True)
    good_name = models.CharField(max_length=255, null=True)
    code_1 = models.CharField(max_length=100, null=True)
    quantity = models.FloatField(default=0)
    sales_doc_name = models.CharField(max_length=255, default='Расходная накладная')
    sales_doc_no = models.CharField(max_length=20, null=True)
    sales_doc_date = models.DateField(default=datetime.date(2000, 1, 1))
    buy_without_vat = models.FloatField(default=0)
    buy_with_vat = models.FloatField(default=0)
    sales_quantity = models.FloatField(default=0)
    sale_without_vat = models.FloatField(default=0)
    sale_with_vat = models.FloatField(default=0)
    sale_price_vat = models.FloatField(default=0)
    customer_name = models.CharField(max_length=255, null=True)
    customer_frigat_id = models.IntegerField(null=True)
    customer_all = models.ForeignKey(Customer, models.SET_NULL, null=True)
    sales_doc = models.ForeignKey(SalesDoc, models.SET_NULL, null=True, db_index=True)

    def __repr__(self):
        return self.code

    def __str__(self):
        return str(self.code)


