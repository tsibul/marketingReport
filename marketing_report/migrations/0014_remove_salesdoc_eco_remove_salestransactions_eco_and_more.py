# Generated by Django 4.2.4 on 2024-02-08 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0013_businessunit_crmtype_business_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesdoc',
            name='eco',
        ),
        migrations.RemoveField(
            model_name='salestransactions',
            name='eco',
        ),
        migrations.AddField(
            model_name='salesdoc',
            name='business_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.businessunit'),
        ),
        migrations.AddField(
            model_name='salestransactions',
            name='business_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.businessunit'),
        ),
    ]
