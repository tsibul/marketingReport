from datetime import timedelta

from django.db.models import F, Func, Value, CharField

from marketing_report.models import CustomerGroup


def cst_migrations(periods, parameter):
    date_format = '%d.%m.%y'
    parameter_number = int(parameter)
    res = []
    for period in periods:
        first_date = period.date_begin
        last_date = period.date_end
        last_client_date = last_date - timedelta(days=parameter_number * 365)
        first_client_date = first_date - timedelta(days=parameter_number * 365)
        customers_finished = CustomerGroup.objects.filter(
            date_last__gte=first_client_date,
            date_last__lte=last_client_date
        ).annotate(
            date=Func(
                F('date_first'),
                Value(date_format),
                function='DATE_FORMAT',
                output_field=CharField()
            )
        ).values('name', 'date')

        customers_new = CustomerGroup.objects.filter(
            date_first__gte=first_date,
            date_first__lte=last_date
        ).annotate(
            date=Func(
                F('date_first'),
                Value(date_format),
                function='DATE_FORMAT',
                output_field=CharField()
            )
        ).values('name', 'date')

        customers_current = CustomerGroup.objects.filter(
            date_first__lt=first_date,
            date_last__gt=last_client_date
        ).annotate(
            date=Func(
                F('date_first'),
                Value(date_format),
                function='DATE_FORMAT',
                output_field=CharField()
            )
        ).values('name', 'date')
        res.append({'period': period.name,
                    'newQuant': customers_new.count(),
                    'currentQuant': customers_current.count() + customers_new.count(),
                    'finishQuant': customers_finished.count(),
                    'customersFinished': list(customers_finished),
                    'customersNew': list(customers_new),
                    'customersCurrent': list(customers_current)})
    return res
