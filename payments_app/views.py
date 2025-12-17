import uuid
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Payment


def create_vip_payment(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.FRONTEND_URL}/login.html")

    user = request.user
    amount = 1000

    shop_order_number = str(uuid.uuid4())

    Payment.objects.create(
        user=user,
        amount=amount,
        shop_order_number=shop_order_number,
        status="PENDING",
    )

    portmone_url = "https://www.portmone.com.ua/gateway/"

    success_url = (
        request.build_absolute_uri("/payments/vip/success/")
        + f"?shop_order_number={shop_order_number}"
    )

    failure_url = request.build_absolute_uri("/payments/vip/failure/")

    data = {
        "payee_id": settings.PORTMONE_PAYEE_ID,
        "shop_order_number": shop_order_number,
        "bill_amount": amount,
        "description": "VIP subscription",
        "success_url": success_url,
        "failure_url": failure_url,
        "lang": "uk",
        "encoding": "UTF-8",
    }

    query = "&".join(f"{k}={v}" for k, v in data.items())
    return redirect(f"{portmone_url}?{query}")


@csrf_exempt
def payment_success(request):

    payment = None

    shop_order_number = (
        request.GET.get("SHOPORDERNUMBER")
        or request.POST.get("SHOPORDERNUMBER")
    )

    if shop_order_number:
        payment = Payment.objects.filter(
            shop_order_number=shop_order_number
        ).first()

    if not payment:
        payment = Payment.objects.filter(
            status="PENDING"
        ).order_by("-created_at").first()

    if payment:
        payment.status = "SUCCESS"
        payment.save()

        user = payment.user
        user.status = "VIP"
        user.save()

    return redirect(f"{settings.FRONTEND_URL}/main_page.html?vip=success")


@csrf_exempt
def payment_failure(request):
    return redirect(f"{settings.FRONTEND_URL}/main_page.html?vip=error")
