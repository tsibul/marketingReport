# Generated by Django 4.2.4 on 2023-10-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing_report', '0007_color_deleted_colorscheme_deleted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportCustomers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frigat_id', models.IntegerField(db_index=True)),
                ('form', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('inn', models.CharField(max_length=20, null=True)),
                ('customer_type', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('all_phones', models.CharField(blank=True, max_length=600, null=True)),
                ('mail', models.CharField(blank=True, max_length=255, null=True)),
                ('all_mails', models.CharField(blank=True, max_length=600, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('our_manager', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]