# Generated by Django 4.2.4 on 2024-02-10 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0015_salesperiodbusinessunit_salesperiod'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('cost_without_vat', models.FloatField(default=0)),
                ('profit', models.FloatField(default=0)),
                ('price_with_vat', models.FloatField(default=0)),
                ('sale_with_vat', models.FloatField(default=0)),
                ('sale_without_vat', models.FloatField(default=0)),
                ('sales_no', models.FloatField(default=0)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_report.goods')),
                ('main_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='marketing_report.color')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing_report.reportperiod')),
            ],
            options={
                'verbose_name': 'periods where was sales of goods',
            },
        ),
    ]
