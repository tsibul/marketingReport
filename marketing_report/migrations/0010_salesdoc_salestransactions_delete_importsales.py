# Generated by Django 4.2.4 on 2024-02-08 06:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0009_importsales_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_doc_number', models.CharField(max_length=20, null=True)),
                ('sales_doc_date', models.DateField(default=datetime.date(2000, 1, 1))),
                ('customer_frigat_id', models.IntegerField(null=True)),
                ('quantity', models.FloatField(default=0)),
                ('sale_with_vat', models.FloatField(default=0)),
                ('sale_without_vat', models.FloatField(default=0)),
                ('purchase_with_vat', models.FloatField(default=0)),
                ('purchase_without_vat', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('no_vat', models.BooleanField(default=False)),
                ('good_no_error', models.BooleanField(default=True)),
                ('eco', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customer')),
                ('month', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='month_%(class)s', to='marketing_report.reportperiod')),
                ('quarter', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_%(class)s', to='marketing_report.reportperiod')),
                ('year', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='year_%(class)s', to='marketing_report.reportperiod')),
            ],
            options={
                'verbose_name': 'отгрузочные документы',
            },
        ),
        migrations.CreateModel(
            name='SalesTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_doc_number', models.CharField(max_length=20, null=True)),
                ('sales_doc_date', models.DateField(default=datetime.date(2000, 1, 1))),
                ('customer_frigat_id', models.IntegerField(null=True)),
                ('quantity', models.FloatField(default=0)),
                ('sale_with_vat', models.FloatField(default=0)),
                ('sale_without_vat', models.FloatField(default=0)),
                ('purchase_with_vat', models.FloatField(default=0)),
                ('purchase_without_vat', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('no_vat', models.BooleanField(default=False)),
                ('import_date', models.DateField(default=datetime.date(2024, 1, 31))),
                ('code', models.CharField(max_length=140)),
                ('color_code', models.CharField(max_length=60, null=True)),
                ('main_color', models.CharField(max_length=60, null=True)),
                ('price_vat', models.FloatField(default=0)),
                ('customer_name', models.CharField(max_length=255, null=True)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.color')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customer')),
                ('goods', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.goods')),
                ('month', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='month_%(class)s', to='marketing_report.reportperiod')),
                ('quarter', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_%(class)s', to='marketing_report.reportperiod')),
                ('sales_doc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.salesdoc')),
                ('year', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='year_%(class)s', to='marketing_report.reportperiod')),
            ],
            options={
                'verbose_name': 'common sales info',
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='ImportSales',
        ),
    ]
