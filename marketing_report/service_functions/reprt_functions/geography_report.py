from django.db.models import Sum, F
from django.db.models.functions import Round

from marketing_report.models import CustomerPeriodByUnit, FedRegion, BusinessUnit, CustomerPeriod, CustomerGroup


def cst_geography(periods, parameter):
    data = CustomerPeriodByUnit.objects.filter(
        period__in=periods,
        customer__internal=False,
        customer__fed_region__isnull=False,
        business_unit__isnull=False
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

    data_region_total = CustomerPeriodByUnit.objects.filter(
        period__in=periods,
        customer__internal=False,
        customer__fed_region__isnull=False,
        business_unit__isnull=False
    ).values(
        'customer__fed_region__name',
        'period__name'
    ).annotate(
        quantity_s=Round(Sum('quantity') / 1000, 2),
        sales_without_vat_s=Round(Sum('sales_without_vat') / 1000, 2),
        sales_with_vat_s=Round(Sum('sales_with_vat') / 1000, 2),
        profit_s=Round(Sum('profit') / 1000, 2),
        no_sales_s=Sum('no_sales'),
        average_check_s=Round(Sum('sales_with_vat') / Sum('no_sales') / 1000, 2)
    ).order_by('customer__fed_region__name', 'period__date_begin')

    data_unit = CustomerPeriodByUnit.objects.filter(
        period__in=periods,
        customer__internal=False,
        customer__fed_region__isnull=False,
        business_unit__isnull = False
    ).values(
        'customer__fed_region__name',
        'business_unit__name',
        'period__name'
    ).annotate(
        quantity_s=Round(Sum('quantity') / 1000, 2),
        sales_without_vat_s=Round(Sum('sales_without_vat') / 1000, 2),
        sales_with_vat_s=Round(Sum('sales_with_vat') / 1000, 2),
        profit_s=Round(Sum('profit') / 1000, 2),
        no_sales_s=Sum('no_sales'),
        average_check_s=Round(Sum('sales_with_vat') / Sum('no_sales') / 1000, 2)
    ).order_by('customer__fed_region__name', 'business_unit__name', 'period__date_begin')

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

    unit_old = data_unit.first()
    unit_list = []
    for unit in data_unit:
        if unit['customer__fed_region__name'] == unit_old['customer__fed_region__name']:
            if unit['business_unit__name'] == unit_old['business_unit__name']:
                unit_list.append(unit)
            else:
                item =list(filter(lambda x: list(x.keys())[0] == unit_old['business_unit__name'],
                              regions[unit['customer__fed_region__name']]))[0]
                item['unit_sales'] = unit_list
                unit_list = []
                unit_old = unit
                unit_list.append(unit)
        else:
            item = list(filter(lambda x: list(x.keys())[0] == unit_old['business_unit__name'],
                          regions[unit['customer__fed_region__name']]))[0]
            item['unit_sales'] = unit_list
            unit_list = []
            unit_old = unit
            unit_list.append(unit)
        item = list(filter(lambda x: list(x.keys())[0] == unit_old['business_unit__name'],
                           regions[unit['customer__fed_region__name']]))[0]
        item['unit_sales'] = unit_list

    reg_old = data_region_total.first()
    regs = []
    for reg in data_region_total:
        if reg['customer__fed_region__name'] == reg_old['customer__fed_region__name']:
            regs.append(reg)
        else:
            regions[reg_old['customer__fed_region__name']].append({'region_sales': regs})
            regs = []
            reg_old['customer__fed_region__name'] = reg['customer__fed_region__name']
            regs.append(reg)
    regions[reg['customer__fed_region__name']].insert(0, {'region_sales': regs})

    return regions
