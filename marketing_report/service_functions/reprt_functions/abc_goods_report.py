from django.db.models import Sum, F, Min, Q
from django.db.models.functions import Round

from marketing_report.models import GoodsPeriod, Goods, Color


def goods_abc(periods, parameter):
    goods_period_filtered = GoodsPeriod.objects.filter(period__in=periods)
    goods_t = list(goods_period_filtered.values_list('good__item_code', flat=True).distinct())

    totals = goods_totals(goods_period_filtered, goods_t, 'Всего')
    total_period_sales = totals['totals']['goods_total_sales']

    goods_total_sales = standard_annotate(goods_period_filtered.values(
        'good'
    )).order_by(
        '-goods_total_sales'
    )

    sales_current = 0
    goods_a = []
    goods_b = []
    goods_c = []
    for good in goods_total_sales:
        current_good = Goods.objects.filter(id=good['good']).first().item_code if Goods.objects.filter(
            id=good['good']).first() else None
        if sales_current < total_period_sales * 0.75:
            goods_a.append(current_good)
        elif sales_current < total_period_sales * 0.95:
            goods_b.append(current_good)
        else:
            goods_c.append(current_good)
        sales_current += good['goods_total_sales']

    totals_a = goods_totals(goods_period_filtered, goods_a, 'Группа A')
    totals_b = goods_totals(goods_period_filtered, goods_b, 'Группа B')
    totals_c = goods_totals(goods_period_filtered, goods_c, 'Группа C')

    totals_a.update({'goods': []})
    totals_b.update({'goods': []})
    totals_c.update({'goods': []})
    for good in goods_a:
        totals_a['goods'].append(single_good_totals(goods_period_filtered, good))
    for good in goods_b:
        totals_b['goods'].append(single_good_totals(goods_period_filtered, good))
    for good in goods_c:
        totals_c['goods'].append(single_good_totals(goods_period_filtered, good))

    return [totals, totals_a, totals_b, totals_c]


def goods_totals(goods_period_filtered, goods_t, text):
    grand_total_sales = standard_aggregate(goods_period_filtered.filter(
        good__item_code__in=goods_t
    ))
    grand_total_period_sales = standard_annotate(goods_period_filtered.filter(
        good__item_code__in=goods_t
    ).values(
        'period__name'
    ))

    return {'name': text, 'periods': list(grand_total_period_sales), 'totals': grand_total_sales}


def single_good_totals(goods_period_filtered, good):
    good_name = Goods.objects.get(item_code=good).item_code if Goods.objects.filter(item_code=good) else None
    grand_total_sales = standard_aggregate(goods_period_filtered.filter(
        good__item_code=good
    ))
    grand_total_period_sales = standard_annotate(goods_period_filtered.filter(
        good__item_code=good
    ).values(
        'period__name'
    ))
    total_good_sales = grand_total_sales['goods_total_sales']

    color_total_sales = standard_annotate(goods_period_filtered.filter(
        good__item_code=good
    ).values(
        'main_color'
    )).order_by(
        '-goods_total_sales'
    )
    sales_current = 0
    colors_a = []
    colors_b = []
    colors_c = []
    for color in color_total_sales:
        current_color = Color.objects.get(id=color['main_color']).code if Color.objects.filter(
            id=color['main_color']) else None
        if sales_current < total_good_sales * 0.75:
            colors_a.append(current_color)
        elif sales_current < total_good_sales * 0.95:
            colors_b.append(current_color)
        else:
            colors_c.append(current_color)
        sales_current += color['goods_total_sales']

    total_colors_a = color_totals(goods_period_filtered, colors_a, good, 'Цвета A')
    total_colors_b = color_totals(goods_period_filtered, colors_b, good, 'Цвета B')
    total_colors_c = color_totals(goods_period_filtered, colors_c, good, 'Цвета C')

    total_colors_a.update({'colors': []})
    total_colors_b.update({'colors': []})
    total_colors_c.update({'colors': []})
    for color in colors_a:
        total_colors_a['colors'].append(single_color_totals(goods_period_filtered, color, good))
    for color in colors_b:
        total_colors_b['colors'].append(single_color_totals(goods_period_filtered, color, good))
    for color in colors_c:
        total_colors_c['colors'].append(single_color_totals(goods_period_filtered, color, good))

    return {'name': good_name, 'periods': list(grand_total_period_sales), 'totals': grand_total_sales,
            'colors_a': total_colors_a, 'colors_b': total_colors_b, 'colors_c': total_colors_c}


def color_totals(goods_period_filtered, colors_t, good, text):
    grand_total_sales = standard_aggregate(goods_period_filtered.filter(
        good__item_code=good,
        main_color__code__in=colors_t
    ))
    grand_total_period_sales = standard_annotate(goods_period_filtered.filter(
        good__item_code=good,
        main_color__code__in=colors_t
    ).values(
        'period__name'
    ))

    return {'name': text, 'periods': list(grand_total_period_sales), 'totals': grand_total_sales}


def single_color_totals(goods_period_filtered, color, good):
    good = Goods.objects.filter(item_code=good).first()
    if good:
        color_group = good.color_scheme
        if Color.objects.filter(code=color):
            try:
                color_name = Color.objects.get(code=color, color_scheme=color_group).code
            except:
                color_name = Color.objects.filter(code=color).first().code
        else:
            color_name = None
    else:
        if Color.objects.filter(code=color):
            color_name = Color.objects.filter(code=color).first().code
        else:
            color_name = None
    grand_total_sales = standard_aggregate(goods_period_filtered.filter(
        good__item_code=good,
        main_color__code=color
    ))
    grand_total_period_sales = standard_annotate(goods_period_filtered.filter(
        good__item_code=good,
        main_color__code=color
    ).values(
        'period__name'
    ))

    return {'name': color_name, 'periods': list(grand_total_period_sales), 'totals': grand_total_sales}


def standard_annotate(custom_query):
    return custom_query.annotate(
        goods_total_sales=Round(Sum('sales_without_vat') / 1000, 2),
        goods_total_quantity=Round(Sum('quantity') / 1000, 2),
        goods_total_no_sales=Round(Sum('sales_no') / 1000, 2),
        goods_average_price=Round(Sum('sales_with_vat') / Sum('quantity'), 2),
        goode_average_sales_quantity=Round(Sum('quantity') / Sum('sales_no') / 1000, 2),
        goods_minimal_quantity=Min('quantity', filter=~Q(quantity__lte=10))
    )


def standard_aggregate(custom_query):
    return custom_query.aggregate(
        goods_total_sales=Round(Sum('sales_without_vat') / 1000, 2),
        goods_total_quantity=Round(Sum('quantity') / 1000, 2),
        goods_total_no_sales=Round(Sum('sales_no') / 1000, 2),
        goods_average_price=Round(Sum('sales_with_vat') / Sum('quantity'), 2),
        goode_average_sales_quantity=Round(Sum('quantity') / Sum('sales_no') / 1000, 2),
        goods_minimal_quantity=Min('quantity', filter=~Q(quantity__lte=10))
    )
