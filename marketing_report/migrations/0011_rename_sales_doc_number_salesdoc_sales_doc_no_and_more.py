# Generated by Django 4.2.4 on 2024-02-08 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0010_salesdoc_salestransactions_delete_importsales'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesdoc',
            old_name='sales_doc_number',
            new_name='sales_doc_no',
        ),
        migrations.RenameField(
            model_name='salestransactions',
            old_name='sales_doc_number',
            new_name='sales_doc_no',
        ),
    ]
