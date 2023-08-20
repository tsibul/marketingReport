import datetime
import calendar
from django.db import models


from django.utils.translation import gettext_lazy as _


month_rus = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}


class ReportPeriod(models.Model):
    class Periods(models.TextChoices):
        MONTH = 'MT', _('месяц')
        QUARTER = 'QT', _('квартал')
        YEAR = 'YR', _('год')

        def __repr__(self):
            return self.label

        def __str__(self):
            return self.label

    period = models.CharField(max_length=2, choices=Periods.choices, default=Periods.MONTH)
    date_begin = models.DateField(default=datetime.date(2000, 1, 1))
    date_end = models.DateField(default=datetime.date(2000, 1, 31))
    name = models.CharField(max_length=100)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def calculable_list(cls):
        return [cls.Periods.MONTH, cls.Periods.QUARTER, cls.Periods.YEAR]

    def set_period(self, date_begin: datetime, name):
        if isinstance(name, str):
            if name == 'MT':
                self.period = self.Periods.MONTH
                self.date_begin = date_begin.replace(day=1)
                self.date_end = datetime.date(date_begin.year, date_begin.month,
                                              calendar.monthrange(date_begin.year, date_begin.month)[-1])
                self.name = month_rus[self.date_begin.month] + ' ' + str(self.date_begin.year)

            elif name == 'QT':
                self.period = self.Periods.QUARTER
                quarter = (date_begin.month - 1) // 3 + 1
                self.date_begin = datetime.date(date_begin.year, 3 * quarter - 2, 1)
                self.date_end = datetime.date(date_begin.year, 3 * quarter, 30 if quarter in [2, 3] else 31)
                self.name = str(quarter) + ' ' + self.period.QUARTER.label + ' ' + str(self.date_begin.year)

            elif name == 'YR':
                self.period = self.Periods.YEAR
                self.date_begin = datetime.date(date_begin.year, 1, 1)
                self.date_end = datetime.date(date_begin.year, 12, 31)
                self.name = str(self.date_begin.year)

    def copy(self):
        return ReportPeriod(period=self.period, date_begin=self.date_begin, date_end=self.date_end, name=self.name)

    def plus(self, n: int):

        if self.period == 'MT':
            year_n = self.date_begin.year + 1 if self.date_begin.month + n > 12 else self.date_begin.year
            self.date_begin = datetime.date(year_n,
                                            (self.date_begin.month + n) % 12 if self.date_begin.month + n != 12 else 12,
                                            1)
            self.date_end = datetime.date(self.date_begin.year, self.date_begin.month,
                                          calendar.monthrange(self.date_begin.year, self.date_begin.month)[-1])
            self.name = month_rus[self.date_begin.month] + ' ' + str(self.date_begin.year)
        elif self.period == 'QT':
            year_n = self.date_begin.year + 1 if self.date_begin.month + 3 * n > 12 else self.date_begin.year
            qr = ((self.date_begin.month - 1 + 3 * n) // 3 + 1)
            quarter = qr % 4 if qr % 4 != 0 else 4
            self.date_begin = datetime.date(year_n, 3 * quarter - 2, 1)
            self.date_end = datetime.date(year_n, 3 * quarter, 30 if quarter in [2, 3] else 31)
            self.name = str(quarter) + ' ' + self.period.QUARTER.label + ' ' + str(self.date_begin.year)
        elif self.period == 'YR':
            self.date_begin = datetime.date(self.date_begin.year + n, 1, 1)
            self.date_end = datetime.date(self.date_begin.year, 12, 31)
            self.name = str(self.date_begin.year)
