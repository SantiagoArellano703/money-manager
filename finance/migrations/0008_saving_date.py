# Generated by Django 4.2.13 on 2024-06-13 21:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_saving'),
    ]

    operations = [
        migrations.AddField(
            model_name='saving',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
