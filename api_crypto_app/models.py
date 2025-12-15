from django.db import models

class CryptoCurrencyPrice(models.Model):
    symbol = models.CharField(max_length=10)
    blockchain = models.CharField(max_length=40)
    address = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=40, decimal_places=20)
    yesterday_price = models.DecimalField(max_digits=40, decimal_places=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']