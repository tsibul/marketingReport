# Generated by Django 4.2.4 on 2024-02-04 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0012_alter_importcustomers_changed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colorscheme',
            old_name='scheme_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='customertypes',
            old_name='type_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='goodcrmtype',
            old_name='crm_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='goodmatrixtype',
            old_name='matrix_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='printtype',
            old_name='type_name',
            new_name='name',
        ),
    ]