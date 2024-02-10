import csv
import datetime

from django.db.models import Sum, Max, Min

from marketing_report.models import SalesTransactions, Customer, Goods, Color, SalesDoc, find_all_period_by_date_range, \
    ReportPeriod, BusinessUnit, create_sales_period, create_sales_period_business_unit, create_goods_period


def sales_import_management():
    min_date, max_date = sales_to_sales_transactions()
    sales_transactions_query = SalesTransactions.objects.filter(
        sales_doc_date__gte=min_date,
        sales_doc_date__lte=max_date
    )
    sales_to_sales_doc(min_date, max_date, sales_transactions_query)
    sales_docs_query = SalesDoc.objects.filter(
        sales_doc_date__gte=min_date,
        sales_doc_date__lte=max_date
    )
    periods = find_all_period_by_date_range(min_date, max_date)
    create_sales_period(periods, sales_docs_query)
    create_sales_period_business_unit(periods, sales_docs_query)
    create_goods_period(periods, sales_transactions_query)


def sales_to_sales_transactions():
    """импорт данных о продажах во временную базу"""
    # ImportSales.objects.all().delete()
    sales = []
    min_date = datetime.datetime.strptime('01.01.2500', '%d.%m.%Y')
    max_date = datetime.datetime.strptime('01.01.1900', '%d.%m.%Y')
    with open('marketing_report/uploaded/sales.csv', newline='', encoding='utf-8', errors='replace') as sales_csv:
        csv_reader = csv.reader(sales_csv, delimiter=';')
        for row in csv_reader:
            try:
                (full_code, _, _, _, _, _, _, _, _, _, quantity, _, sales_doc_no, sales_doc_date, purchase_without_vat,
                 purchase_with_vat, sale_without_vat, _, sale_with_vat, price_vat, customer_frigat_id,
                 customer_name) = row
                customer = Customer.objects.filter(frigat_code=customer_frigat_id).first()
                full_code_list = full_code.split('.')
                code = full_code_list[0]
                if len(full_code_list) > 2:
                    main_color = full_code_list[1] if len(full_code_list) > 1 else full_code_list[2]
                elif len(full_code_list) == 2 and len(full_code_list[1]) > 1:
                    main_color = full_code_list[1]
                else:
                    main_color = None
                goods = Goods.objects.filter(item_code=code).first()
                color_code = full_code[len(code) + 1:]
                color = Color.objects.filter(code=main_color).first()
                no_vat = sale_with_vat == sale_without_vat
                sales_doc_date = datetime.datetime.strptime(sales_doc_date, '%d.%m.%Y')
                if sales_doc_date > max_date:
                    max_date = sales_doc_date
                if sales_doc_date < min_date:
                    min_date = sales_doc_date
                goods_no_error = True if goods else False
                sale = SalesTransactions(
                    import_date=datetime.date.today(),
                    code=full_code,
                    goods=goods,
                    color_code=color_code,
                    main_color=main_color,
                    color=color,
                    quantity=quantity.replace(',', '.'),
                    sales_doc_no=sales_doc_no,
                    sales_doc_date=sales_doc_date,
                    purchase_without_vat=purchase_without_vat.replace(',', '.'),
                    purchase_with_vat=purchase_with_vat.replace(',', '.'),
                    sale_without_vat=sale_without_vat.replace(',', '.'),
                    sale_with_vat=sale_with_vat.replace(',', '.'),
                    price_vat=price_vat.replace(',', '.'),
                    customer_frigat_id=customer_frigat_id,
                    customer_name=customer_name.replace('"', ''),
                    customer=customer,
                    no_vat=no_vat,
                    good_no_error=goods_no_error,
                    profit=float(sale_without_vat.replace(',', '.')) - float(purchase_without_vat.replace(',', '.')),
                    business_unit=goods.crm_type.business_unit
                )
                sale.set_periods()
                sales.append(sale)
            except Exception as e:
                print(f"ошибка в записи {e}")
    SalesTransactions.objects.filter(sales_doc_date__gte=min_date, sales_doc_date__lte=max_date).delete()
    SalesTransactions.objects.bulk_create(sales)
    return min_date.date(), max_date.date()


def sales_to_sales_doc(min_date, max_date, sales_transactions_query):
    sales_doc_query = sales_transactions_query.values(
        'sales_doc_no', 'sales_doc_date', 'customer', 'no_vat', 'month', 'quarter', 'year'
    ).annotate(
        good_no_error=Min('good_no_error'),
        quantity=Sum('quantity'),
        sale_with_vat=Sum('sale_with_vat'),
        sale_without_vat=Sum('sale_without_vat'),
        purchase_with_vat=Sum('purchase_with_vat'),
        purchase_without_vat=Sum('purchase_without_vat'),
        profit=Sum('profit'),
        business_unit=Max('business_unit'),
    ).order_by('sales_doc_date', 'sales_doc_no')
    sales_docs = list(map(lambda item: SalesDoc(
        sales_doc_no=item['sales_doc_no'],
        sales_doc_date=item['sales_doc_date'],
        customer=Customer.objects.get(id=item['customer']),
        customer_frigat_id=Customer.objects.get(id=item['customer']).frigat_code,
        no_vat=item['no_vat'],
        good_no_error=item['good_no_error'],
        month=ReportPeriod.objects.get(id=item['month']),
        quarter=ReportPeriod.objects.get(id=item['quarter']),
        year=ReportPeriod.objects.get(id=item['year']),
        quantity=item['quantity'],
        sale_with_vat=item['sale_with_vat'],
        sale_without_vat=item['sale_without_vat'],
        purchase_with_vat=item['purchase_with_vat'],
        purchase_without_vat=item['purchase_without_vat'],
        profit=item['profit'],
        business_unit=BusinessUnit.objects.get(id=item['business_unit'])
    ), sales_doc_query))
    SalesDoc.objects.filter(sales_doc_date__gte=min_date, sales_doc_date__lte=max_date).delete()
    SalesDoc.objects.bulk_create(sales_docs)

# Subquery(
#     SalesTransactions.objects.filter(
#         sales_doc_date__gte=min_date,
#         sales_doc_date__lte=max_date,
#         business_unit=OuterRef('business_unit')
#     ).values('business_unit').annotate(count=Count('business_unit')).order_by('-count')[:1].values(
#         'business_unit')
# )
