from django.db import models


class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "category"
