# Generated by Django 4.2.4 on 2024-02-04 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='color',
            old_name='color_code',
            new_name='hex',
        ),
    ]
