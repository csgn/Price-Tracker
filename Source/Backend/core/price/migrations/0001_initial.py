# Generated by Django 3.2.9 on 2021-11-22 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('priceid', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField(null=True)),
                ('startdate', models.DateTimeField()),
                ('productid', models.ForeignKey(db_column='productid', on_delete=django.db.models.deletion.RESTRICT, to='product.product')),
                ('supplierid', models.ForeignKey(db_column='supplierid', on_delete=django.db.models.deletion.RESTRICT, to='supplier.supplier')),
            ],
            options={
                'db_table': 'price',
            },
        ),
    ]
