from django.db import models


class Supplier(models.Model):
    supplierid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    rate = models.FloatField(null=True)
    url = models.URLField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "supplier"
