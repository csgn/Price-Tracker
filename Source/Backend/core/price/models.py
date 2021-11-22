from django.db import models

from supplier.models import Supplier
from product.models import Product


class Price(models.Model):
    priceid = models.AutoField(primary_key=True)
    amount = models.FloatField(null=True)
    startdate = models.DateTimeField()
    supplierid = models.ForeignKey(
        to=Supplier, on_delete=models.RESTRICT, db_column="supplierid")
    productid = models.ForeignKey(
        to=Product, on_delete=models.RESTRICT, db_column="productid"
    )

    def __str__(self) -> str:
        return str(self.supplierid) + ' | ' + str(self.productid) + ' | ' + str(self.amount) + ' TL'

    class Meta:
        db_table = "price"
