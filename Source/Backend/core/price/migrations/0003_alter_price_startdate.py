# Generated by Django 3.2.9 on 2021-11-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0002_alter_price_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='startdate',
            field=models.DateTimeField(),
        ),
    ]
