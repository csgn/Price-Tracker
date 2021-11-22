from django.db import models
from django.contrib.postgres import fields as ps_models

from category.models import Category
from brand.models import Brand


class Product(models.Model):
    productid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    images = ps_models.ArrayField(
        models.URLField()
    )
    rate = models.FloatField(null=True)
    url = models.URLField()
    brandid = models.ForeignKey(
        to=Brand, on_delete=models.DO_NOTHING, db_column="brandid")
    categoryid = models.ForeignKey(
        to=Category, on_delete=models.DO_NOTHING, db_column="categoryid")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "product"
