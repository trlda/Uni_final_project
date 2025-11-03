from django.urls import path
from .views import DIASymbolPrice

urlpatterns = [
    path("prices/", DIASymbolPrice.as_view(), name="prices"),
]