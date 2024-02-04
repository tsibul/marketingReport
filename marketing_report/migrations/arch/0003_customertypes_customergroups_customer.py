# Generated by Django 4.2.4 on 2023-09-10 23:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0002_colorscheme_goodcrmtype_goodmatrixtype_printgroup_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=30)),
                ('group_discount', models.FloatField(default=0)),
                ('code', models.CharField(default='', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=255, unique=True)),
                ('phone', models.CharField(default='', max_length=255)),
                ('mail', models.CharField(default='', max_length=255)),
                ('date_first', models.DateField(default=datetime.date(2000, 1, 1))),
                ('date_last', models.DateField(default=datetime.date(2000, 1, 1))),
                ('active', models.BooleanField(default=True)),
                ('group_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customertypes')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('inn', models.CharField(max_length=20, null=True)),
                ('region', models.CharField(max_length=2)),
                ('frigat_id', models.CharField(db_index=True, default='', max_length=30)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('all_phones', models.CharField(blank=True, max_length=600, null=True)),
                ('mail', models.CharField(blank=True, max_length=255, null=True)),
                ('all_mails', models.CharField(blank=True, max_length=600, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('our_manager', models.CharField(blank=True, max_length=255)),
                ('date_import', models.DateField(default=datetime.date(2000, 1, 1))),
                ('date_first', models.DateField(default=datetime.date(2000, 1, 1))),
                ('date_last', models.DateField(default=datetime.date(2000, 1, 1))),
                ('active', models.BooleanField(default=True)),
                ('internal', models.BooleanField(default=False)),
                ('customer_group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customergroups')),
                ('customer_type', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customertypes')),
            ],
        ),
    ]