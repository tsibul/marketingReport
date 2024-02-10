import datetime

from django.db import models
from marketing_report.models.report_period import ReportPeriod
from marketing_report.models.customer_models import Customer
from marketing_report.models.goods_models import Goods
from marketing_report.models.color_models import Color
from marketing_report.models.goods_types_models import BusinessUnit


class SalesAbstract(models.Model):
    """
    quantity: количество данной себестоимости [11]
    sales_doc_no: номер документа продажи [13]
    sales_doc_date: дата документа продажи [14]
    purchase_without_vat: сумма без НДС закупки [15]
    purchase_with_vat: сумма с НДС закупки [16]
    sale_without_vat: сумма без НДС продажи [17]
    sale_with_vat: сумма с НДС продажи [19]
    customer_frigat_id: код клиента фрегат [21]
    customer: клиент (ссылка)
    no_vat: если продажа без НДС
    profit: прибыль
    """

    class Meta:
        abstract = True
        verbose_name = 'common sales info'

    sales_doc_no = models.CharField(max_length=20, null=True)
    sales_doc_date = models.DateField(default=datetime.date(2000, 1, 1))
    customer_frigat_id = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    quantity = models.FloatField(default=0)
    sale_with_vat = models.FloatField(default=0)
    sale_without_vat = models.FloatField(default=0)
    purchase_with_vat = models.FloatField(default=0)
    purchase_without_vat = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    no_vat = models.BooleanField(default=False)
    month = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='month_%(class)s')
    quarter = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='quarter_%(class)s')
    year = models.ForeignKey(ReportPeriod, models.SET_NULL, null=True, default='', related_name='year_%(class)s')
    good_no_error = models.BooleanField(default=True)
    business_unit = models.ForeignKey(BusinessUnit, models.SET_NULL, null=True)



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


class SalesDoc(SalesAbstract):
    class Meta:
        verbose_name = 'отгрузочные документы'

    def __repr__(self):
        return str(self.sales_doc_no) + ' от ' + str(self.sales_doc_date)

    def __str__(self):
        return str(self.sales_doc_no) + ' от ' + str(self.sales_doc_date)

    def set_periods(self):
        super().set_periods()

    def save(self, *args, **kwargs):
        self.set_periods()
        super().save(*args, **kwargs)


class SalesTransactions(SalesAbstract):
    """ Frigat fields from report:
    import_date : дата импорта
    code: артикул [1]
    goods: деталь (ссылка)
    color_code: код после артикула детали
    main_color: код главного цвета
    color: главный цвет (ссылка)
    price_vat: цена продажи с НДС [20]
    customer_name: название клиента [22]
    """

    import_date = models.DateField(default=datetime.date(2024, 1, 31))
    code = models.CharField(max_length=140)
    goods = models.ForeignKey(Goods, models.SET_NULL, null=True, db_index=True)
    color_code = models.CharField(max_length=60, null=True)
    main_color = models.CharField(max_length=60, null=True)
    color = models.ForeignKey(Color, models.SET_NULL, null=True)
    price_vat = models.FloatField(default=0)
    customer_name = models.CharField(max_length=255, null=True)
    sales_doc = models.ForeignKey(SalesDoc, models.SET_NULL, null=True)

    def __repr__(self):
        return self.code + 'от' + str(self.sales_doc_date)

    def __str__(self):
        return str(self.code) + 'от' + str(self.sales_doc_date)

    def set_periods(self):
        super().set_periods()

    def save(self, *args, **kwargs):
        self.set_periods()
        super().save(*args, **kwargs)
