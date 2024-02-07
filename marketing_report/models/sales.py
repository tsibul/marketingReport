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
    total_purchase_with_vat = models.FloatField(default=0)
    total_purchase_without_vat = models.FloatField(default=0)
    order = models.CharField(max_length=100, null=True)
    good_no_error = models.BooleanField(default=True)
    eco = models.BooleanField(default=True)
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
        import_date : дата импорта
        code: артикул [1]
        goods: деталь (ссылка)
        color_code: код после артикула детали
        main_color: код главного цвета
        color: главный цвет (ссылка)
        quantity: количество данной себестоимости [11]
        sales_doc_no: номер документа продажи [13]
        sales_doc_date: дата документа продажи [14]
        purchase_without_vat: сумма без НДС закупки [15]
        purchase_with_vat: сумма с НДС закупки [16]
        sale_without_vat: сумма без НДС продажи [17]
        sale_with_vat: сумма с НДС продажи [19]
        price_vat: цена продажи с НДС [20]
        customer_frigat_id: код клиента фрегат [21]
        customer_name: название клиента [22]
        customer: клиент (ссылка)
        """

    import_date = models.DateField(default=datetime.date(2024, 1, 31))
    code = models.CharField(max_length=140)
    goods = models.ForeignKey(Goods, models.SET_NULL, null=True, db_index=True)
    color_code = models.CharField(max_length=60, null=True)
    main_color = models.CharField(max_length=60, null=True)
    color = models.ForeignKey(Color, models.SET_NULL, null=True)
    quantity = models.FloatField(default=0)
    sales_doc_no = models.CharField(max_length=20, null=True)
    sales_doc_date = models.DateField(default=datetime.date(2019, 1, 1))
    purchase_without_vat = models.FloatField(default=0)
    purchase_with_vat = models.FloatField(default=0)
    sale_without_vat = models.FloatField(default=0)
    sale_with_vat = models.FloatField(default=0)
    price_vat = models.FloatField(default=0)
    customer_frigat_id = models.IntegerField(null=True)
    customer_name = models.CharField(max_length=255, null=True)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    no_vat = models.BooleanField(default=False)

    def __repr__(self):
        return self.code

    def __str__(self):
        return str(self.code)
