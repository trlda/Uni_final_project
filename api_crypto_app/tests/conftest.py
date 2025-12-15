import pytest
from rest_framework.test import APIClient

@pytest.fixture(scope="function")
def api_client():
    yield APIClient()

@pytest.fixture(scope="function")
def crypto_symbols():
    yield ["BTC", "ETH", "USDT", "XRP", "BNB", "SOL", "USDC", "stETH", "TRX", "ORDI", "WBTC", "HYPE", "LINK", "SATS"]
