from django.db.models import Sum, F
from django.db.models.functions import Round

from marketing_report.models import CustomerPeriodByUnit, FedRegion, BusinessUnit, CustomerPeriod, CustomerGroup


def cst_geography(periods, parameter):
    data = CustomerPeriodByUnit.objects.filter(
        period__in=periods,
        customer__internal=False,
        customer__fed_region__isnull=False
    ).values(
        'customer__fed_region__name',
        'business_unit__name',
        'customer__customer_group__name',
        'period__name'
    ).annotate(
        quantity_s=Round(Sum('quantity') / 1000, 2),
        sales_without_vat_s=Round(Sum('sales_without_vat') / 1000, 2),
        sales_with_vat_s=Round(Sum('sales_with_vat') / 1000, 2),
        profit_s=Round(Sum('profit') / 1000, 2),
        no_sales_s=Sum('no_sales'),
        average_check_s=Round(Sum('sales_with_vat') / Sum('no_sales') / 1000, 2)
    ).order_by('customer__fed_region__name', 'business_unit__name', 'customer__customer_group__name',
               'period__date_begin')

    region_previous = data.first()['customer__fed_region__name']
    regions = {region_previous: []}
    for item in data:
        if region_previous == item['customer__fed_region__name']:
            regions[region_previous].append(item)
        else:
            region_previous = item['customer__fed_region__name']
            regions[region_previous] = []
            regions[region_previous].append(item)
    for region, region_values in regions.items():
        unit_prev = region_values[0]['business_unit__name']
        units = {unit_prev: []}
        unit_list = []
        for item in region_values:
            if unit_prev == item['business_unit__name']:
                units[unit_prev].append(item)
            else:
                unit_list.append(units)
                unit_prev = item['business_unit__name']
                units = {unit_prev: []}
                units[unit_prev].append(item)
        unit_list.append(units)
        regions[region] = unit_list
    for region, region_values in regions.items():
        for unit in region_values:
            unit_key, unit_value = next(iter(unit.items()))
            cst_prev = unit_value[0]['customer__customer_group__name']
            cst = {cst_prev: []}
            cst_list = []
            for item in unit_value:
                if cst_prev == item['customer__customer_group__name']:
                    cst[cst_prev].append(item)
                else:
                    cst_list.append(cst)
                    cst_prev = item['customer__customer_group__name']
                    cst = {cst_prev: []}
                    cst[cst_prev].append(item)
            cst_list.append(cst)
            unit[unit_key] = cst_list


    return regions
