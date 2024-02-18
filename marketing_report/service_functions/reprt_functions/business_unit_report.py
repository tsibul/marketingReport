from django.db.models import Sum, F
from django.db.models.functions import Round

from marketing_report.models import BusinessUnit, CustomerPeriodByUnit
from marketing_report.models.argument_classes import money_argument_list


# from marketing_report.service_functions.reprt_functions.abc_report import group_customers_by_abc


def business_unit(periods, parameter):
    units = []
    for unit in BusinessUnit.objects.all().order_by('code'):
        parameter_field = (next(filter(lambda param: param.code == parameter, money_argument_list()), None)).field
        total_parameter_field = 'total_' + parameter_field

        grand_total = CustomerPeriodByUnit.objects.filter(
            period__in=periods,
            customer__internal=False,
            business_unit=unit
        ).aggregate(
            total=Round(Sum(parameter_field) / 1000, 2)
        )['total']

        customers = CustomerPeriodByUnit.objects.filter(
            period__in=periods,
            customer__internal=False,
            business_unit=unit
        ).values(
            group_code=F('customer__customer_group__name'),
            period_code=F('period__name')
        ).annotate(
            quantity_s=Round(Sum('quantity') / 1000, 2),
            sales_without_vat_s=Round(Sum('sales_without_vat') / 1000, 2),
            sales_with_vat_s=Round(Sum('sales_with_vat') / 1000, 2),
            profit_s=Round(Sum('profit') / 1000, 2),
            no_sales_s=Sum('no_sales'),
            average_check_s=Round(Sum('sales_with_vat') / Sum('no_sales') / 1000, 2)
        ).order_by('period__date_begin')

        customers_total = CustomerPeriodByUnit.objects.filter(
            period__in=periods,
            customer__internal=False,
            business_unit=unit
        ).values(
            group_code=F('customer__customer_group__name'),
        ).annotate(
            total_quantity=Round(Sum('quantity') / 1000, 2),
            total_sales_without_vat=Round(Sum('sales_without_vat') / 1000, 2),
            total_sales_with_vat=Round(Sum('sales_with_vat') / 1000, 2),
            total_profit=Round(Sum('profit') / 1000, 2),
            total_no_sales=Sum('no_sales'),
            average_check=Round(Sum('sales_with_vat') / Sum('no_sales') / 1000, 2)
        ).order_by('-' + total_parameter_field)
        subtotal = grand_total
        for group in customers_total:
            if subtotal > grand_total * 0.25:
                group['group'] = 'A'
            elif subtotal > grand_total * 0.05:
                group['group'] = 'B'
            else:
                group['group'] = 'C'
            subtotal = subtotal - group[total_parameter_field]
            group_query = customers.filter(
                group_code=group['group_code']
            ).values(
                'period_code',
                'quantity_s',
                'sales_without_vat_s',
                'sales_with_vat_s',
                'profit_s',
                'no_sales_s',
                'average_check_s'
            )
            group['details'] = list(group_query)
        cl = list(customers_total)
        customers_t_names = [c['group_code'] for c in cl]
        customers_a_names = [c['group_code'] for c in filter(lambda c: c['group'] == 'A', cl)]
        customers_b_names = [c['group_code'] for c in filter(lambda c: c['group'] == 'B', cl)]
        customers_c_names = [c['group_code'] for c in filter(lambda c: c['group'] == 'C', cl)]
        customers_a = list(filter(lambda c: c['group'] == 'A', cl))
        customers_b = list(filter(lambda c: c['group'] == 'B', cl))
        customers_c = list(filter(lambda c: c['group'] == 'C', cl))
        res = [group_customers_by_abc(cl, 'T', customers_t_names, periods, unit),
               group_customers_by_abc(customers_a, 'A', customers_a_names, periods, unit),
               group_customers_by_abc(customers_b, 'B', customers_b_names, periods, unit),
               group_customers_by_abc(customers_c, 'C', customers_c_names, periods, unit)]
        unit_dict = {'unit': unit.name, 'unitReport': res}
        units.append(unit_dict)
    return units


def group_customers_by_abc_data(customers, periods, unit):
    return CustomerPeriodByUnit.objects.filter(
        customer__customer_group__name__in=customers,
        period__in=periods,
        business_unit=unit
    ).values(
        'period__name'
    ).annotate(
        group_quantity=Round(Sum('quantity') / 1000, 2),
        group_sales_without_vat=Round(Sum('sales_without_vat') / 1000, 2),
        group_sales_with_vat=Round(Sum('sales_with_vat') / 1000, 2),
        group_profit=Round(Sum('profit') / 1000, 2),
        group_no_sales=Sum('no_sales'),
        group_average_check=Round(Sum('sales_with_vat') / Sum('no_sales') / 1000, 2)
    ).order_by('period__date_begin')


def group_customers_by_abc(customers, letter, customer_names, periods, unit):
    group_quantity = 0
    group_sales_without_vat = 0
    group_sales_with_vat = 0
    group_profit = 0
    group_no_sales = 0
    customer_quantity = len(customers)
    for cst in customers:
        group_quantity += cst['total_quantity']
        group_sales_without_vat += cst['total_sales_without_vat']
        group_sales_with_vat += cst['total_sales_with_vat']
        group_profit += cst['total_profit']
        group_no_sales += cst['total_no_sales']
    if group_no_sales:
        group_average_check = round(group_sales_with_vat / group_no_sales, 2)
    else:
        group_average_check = 0
    grouped = {
        'group': letter,
        'group_quantity': group_quantity,
        'customer_quantity': customer_quantity,
        'group_sales_without_vat': round(group_sales_without_vat, 2),
        'group_sales_with_vat': round(group_sales_with_vat, 2),
        'group_profit': round(group_profit, 2),
        'group_no_sales': group_no_sales,
        'group_average_check': group_average_check,
        'group_details': list(group_customers_by_abc_data(customer_names, periods, unit)),}
    if letter != 'T':
        grouped.update({'customers': customers})
    return grouped
