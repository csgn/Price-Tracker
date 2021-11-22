# Generated by Django 3.2.9 on 2021-11-22 12:11

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brand', '__first__'),
        ('category', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), size=None)),
                ('rate', models.FloatField(null=True)),
                ('url', models.URLField()),
                ('brandid', models.ForeignKey(db_column='brandid', on_delete=django.db.models.deletion.DO_NOTHING, to='brand.brand')),
                ('categoryid', models.ForeignKey(db_column='categoryid', on_delete=django.db.models.deletion.DO_NOTHING, to='category.category')),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]