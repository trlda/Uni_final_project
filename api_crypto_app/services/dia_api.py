import requests
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)
DIA_BASE_URL = "https://api.diadata.org/v1"

def get_price(symbol):
    cache_key = f"dia_price_{symbol}"

    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache HIT for {cache_key}")
        return cached_data

    logger.info(f"Cache MISS for {cache_key} -> fetch from API")
    url = f"{DIA_BASE_URL}/quotation/{symbol}"
    data = requests.get(url).json()

    filtered_data = {
            'symbol': symbol,
            'blockchain': data.get('Blockchain'),
            'address': data.get('Address'),
            'price': data.get('Price'),
            'yesterday_price': data.get('PriceYesterday')
        }

    if filtered_data['price'] is not None:
        cache.set(cache_key, filtered_data, 7200)
        logger.info(f"Cache SET for {cache_key}")
        return filtered_data
