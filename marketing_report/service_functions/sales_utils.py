import csv
import datetime

from marketing_report.models import ImportSales, Customer, Goods, Color


def sales_to_temp_db():
    """импорт данных о продажах во временную базу"""
    ImportSales.objects.all().delete()
    sales = []
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
                sale = ImportSales(
                    import_date=datetime.date.today(),
                    code=full_code,
                    goods=goods,
                    color_code=color_code,
                    main_color=main_color,
                    color=color,
                    quantity=quantity.replace(',', '.'),
                    sales_doc_no=sales_doc_no,
                    sales_doc_date=datetime.datetime.strptime(sales_doc_date,'%d.%m.%Y'),
                    purchase_without_vat=purchase_without_vat.replace(',', '.'),
                    purchase_with_vat=purchase_with_vat.replace(',', '.'),
                    sale_without_vat=sale_without_vat.replace(',', '.'),
                    sale_with_vat=sale_with_vat.replace(',', '.'),
                    price_vat=price_vat.replace(',', '.'),
                    customer_frigat_id=customer_frigat_id,
                    customer_name=customer_name.replace('"', ''),
                    customer=customer,
                    no_vat=no_vat
                )
                sales.append(sale)
            except Exception as e:
                print(f"ошибка в записи {e}")
    result = ImportSales.objects.bulk_create(sales)
    return len(result)
