# Generated by Django 4.2.4 on 2024-02-10 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0016_goodsperiod'),
    ]

    operations = [
        migrations.AddField(
            model_name='customergroup',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]