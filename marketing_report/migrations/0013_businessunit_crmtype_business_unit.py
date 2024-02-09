# Generated by Django 4.2.4 on 2024-02-08 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0012_salestransactions_eco_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('settingsdictionary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='marketing_report.settingsdictionary')),
                ('code', models.IntegerField(default=0)),
            ],
            bases=('marketing_report.settingsdictionary',),
        ),
        migrations.AddField(
            model_name='crmtype',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketing_report.businessunit'),
        ),
    ]
