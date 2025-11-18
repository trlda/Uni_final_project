import os
import requests
import random
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


def get_btc_balance(address):
    cache_key = f"btc_balance_{address}"
    cached_data = cache.get(cache_key)

    if cached_data:
        logger.info(f"Cache HIT for {cache_key}")
        return cached_data

    logger.info(f"Cache MISS for {cache_key} -> fetch from API")
    url = f"https://blockstream.info/api/address/{address}"

    response = requests.get(url)
    data = response.json()
    chain_stats = data['chain_stats']
    funded = chain_stats['funded_txo_sum']
    spent = chain_stats['spent_txo_sum']
    balance_satoshi = funded - spent
    balance_btc = balance_satoshi / 10 ** 8

    balance = {"balance": balance_btc, "symbol": "BTC"}
    cache.set(cache_key, balance, 3600)
    logger.info(f"Cache SET for {cache_key}")
    return balance


def get_eth_balance(address):
    cache_key = f"eth_balance_{address}"
    cached_data = cache.get(cache_key)

    if cached_data:
        logger.info(f"Cache HIT for {cache_key}")
        return cached_data

    logger.info(f"Cache MISS for {cache_key} -> fetch from API")
    API_KEY = os.getenv("NOWNODES_API_KEY")
    url = f"https://eth.nownodes.io/{API_KEY}"
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": random.randint(1, 999999)
    }

    response = requests.post(url, json=payload)
    data = response.json()

    result_hex = data['result']
    balance_wei = int(result_hex, 16)
    balance_eth = balance_wei / 10 ** 18

    balance = {"balance": balance_eth, "symbol": "ETH"}
    cache.set(cache_key, balance, 3600)
    logger.info(f"Cache SET for {cache_key}")
    return balance

def get_solana_balance(address):
    cache_key = f"sol_balance_{address}"
    cached_data = cache.get(cache_key)

    if cached_data:
        logger.info(f"Cache HIT for {cache_key}")
        return cached_data

    logger.info(f"Cache MISS for {cache_key} -> fetch from API")
    url = "https://api.mainnet-beta.solana.com"
    payload = {
        "jsonrpc": "2.0",
        "id": random.randint(1, 999999),
        "method": "getBalance",
        "params": [address]
    }

    response = requests.post(url, json=payload)
    data = response.json()

    result = data['result']
    balance_lamp = result['value']
    balance_sol = balance_lamp / 10 ** 9

    balance = {"balance": balance_sol, "symbol": "SOL"}
    cache.set(cache_key, balance, 3600)
    logger.info(f"Cache SET for {cache_key}")
    return balance