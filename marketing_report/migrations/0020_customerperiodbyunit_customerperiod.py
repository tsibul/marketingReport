# Generated by Django 4.2.4 on 2024-02-11 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0019_alter_customergroupfrigateid_frigate_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerPeriodByUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='количество')),
                ('sales_without_vat', models.FloatField(default=0, null=True)),
                ('sales_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи с НДС')),
                ('profit', models.FloatField(default=0, null=True, verbose_name='прибыль')),
                ('no_sales', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')),
                ('average_check', models.FloatField(default=0, null=True, verbose_name='средний чек')),
                ('business_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_report.businessunit')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customer')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_report.reportperiod')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='количество')),
                ('sales_without_vat', models.FloatField(default=0, null=True)),
                ('sales_with_vat', models.FloatField(default=0, null=True, verbose_name='продажи с НДС')),
                ('profit', models.FloatField(default=0, null=True, verbose_name='прибыль')),
                ('no_sales', models.SmallIntegerField(default=0, null=True, verbose_name='количество продаж')),
                ('average_check', models.FloatField(default=0, null=True, verbose_name='средний чек')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customer')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_report.reportperiod')),
            ],
            options={
                'verbose_name': 'periods where was transactions with Client',
            },
        ),
    ]
