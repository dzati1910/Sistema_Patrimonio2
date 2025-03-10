# Generated by Django 5.1.6 on 2025-02-18 02:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_alter_supplier_contact_alter_supplier_tax_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='contact',
            field=models.IntegerField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator('^\\d{14}$', 'O campo deve conter exatamente 14 dígitos numéricos')]),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='tax_id',
            field=models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator('^\\d{14}$', 'O campo deve conter exatamente 14 dígitos numéricos')]),
        ),
    ]
