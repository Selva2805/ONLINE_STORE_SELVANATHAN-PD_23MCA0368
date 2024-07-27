from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    customer_id = models.CharField(max_length=50)
    order_date = models.DateField()
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order {self.order_id}"