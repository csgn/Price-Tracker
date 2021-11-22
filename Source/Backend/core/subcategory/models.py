from django.db import models

from category.models import Category


class Subcategory(models.Model):
    subcategoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    categoryid = models.ForeignKey(
        to=Category, on_delete=models.DO_NOTHING, db_column="categoryid")

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "subcategory"
