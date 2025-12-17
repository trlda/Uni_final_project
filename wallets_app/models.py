from django.conf import settings
from django.db import models

class Wallet(models.Model):
    WALLET_CHOICES = (
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("SOL", "Solana"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallets"
    )
    symbol = models.CharField(max_length=5, choices=WALLET_CHOICES)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "symbol")

    def __str__(self):
        return f"{self.user.username} - {self.symbol}"
