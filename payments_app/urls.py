from django.urls import path
from .views import create_vip_payment, payment_success, payment_failure

urlpatterns = [
    path("vip/create/", create_vip_payment, name="vip_create"),
    path("vip/success/", payment_success, name="vip_success"),
    path("vip/failure/", payment_failure, name="vip_failure"),
]
