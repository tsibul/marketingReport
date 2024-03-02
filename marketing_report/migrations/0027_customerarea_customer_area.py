# Generated by Django 4.2.4 on 2024-03-02 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0026_customergroup_fed_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerArea',
            fields=[
                ('settingsdictionary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='marketing_report.settingsdictionary')),
            ],
            bases=('marketing_report.settingsdictionary',),
        ),
        migrations.AddField(
            model_name='customer',
            name='area',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.customerarea'),
        ),
    ]
