from django.db import models

class Sale(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.product} ({self.date})"

    @property
    def total(self):
        return self.unit_price * self.quantity
