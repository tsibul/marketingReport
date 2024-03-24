# Generated by Django 4.2.4 on 2024-03-24 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0028_rename_area_customer_customer_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='customergroup',
            name='business_unit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.businessunit'),
        ),
    ]
