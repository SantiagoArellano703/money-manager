# Generated by Django 4.2.13 on 2024-06-04 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_transaction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('INGRESO', 'Ingreso'), ('GASTO', 'Gasto')], default='INGRESO', max_length=7),
        ),
    ]
