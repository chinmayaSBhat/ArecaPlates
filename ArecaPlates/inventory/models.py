from django.db import models
import uuid
from datetime import date
# Create your models here.
class Stock(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    batch_no=models.IntegerField()
    supplier=models.CharField(max_length=100)
    quantity=models.IntegerField()
    delivery_date=models.DateField(default=date.today)

    def __str__(self) -> str:
        return f"{self.batch_no}"

class Production(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    batch_no=models.ForeignKey(Stock, on_delete=models.CASCADE)
    production_date=models.DateField(default=date.today)
    quantity=models.IntegerField()
    wastage=models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.batch_no.batch_no} -> {self.quantity}"

