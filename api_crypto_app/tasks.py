from background_task import background
from .serializers import CryptoPriceSerializer
from .views import DIASymbolPrice
from .services.dia_api import get_price

curryncies = ["BTC", "ETH", "USDT", "XRP", "BNB", "SOL", "USDC", "stETH", "TRX", "ORDI", "WBTC", "HYPE", "LINK", "SATS"]

@background(schedule=0)
def update_crypto_prices_task():
    for symbol in curryncies:
        price_data = get_price(symbol)
        if price_data:
            serializer = CryptoPriceSerializer(data=price_data)
            if serializer.is_valid():
                serializer.save()

    update_crypto_prices_task(schedule=360)