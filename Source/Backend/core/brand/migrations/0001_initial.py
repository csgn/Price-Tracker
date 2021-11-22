# Generated by Django 3.2.9 on 2021-11-22 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('brandid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
                'db_table': 'brand',
            },
        ),
    ]
