from django.urls import path
from .views import DIASymbolPrice, CheckBalance

urlpatterns = [
    path("prices/", DIASymbolPrice.as_view(), name="prices"),
    path("balance/", CheckBalance.as_view(), name="balance"),
]