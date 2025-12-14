from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.dia_api import get_price
from .services.Api_wallet import get_btc_balance, get_eth_balance, get_solana_balance

curryncies = ["BTC", "ETH", "USDT", "XRP", "BNB", "SOL", "USDC", "stETH", "TRX", "ORDI", "WBTC", "HYPE", "LINK", "SATS"]

class DIASymbolPrice(APIView):
    def get(self, request, format=None):
        symbol = request.query_params.get('symbol')
        
        if symbol:
            data = get_price(symbol)
            if data:
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Price data not found for {symbol}"}, status=status.HTTP_404_NOT_FOUND)
        else:
            result = []
            for symbol in curryncies:
                data = get_price(symbol)
                if data:
                    result.append(data)
            return Response(result, status=status.HTTP_200_OK)


class CheckBalance(APIView):
    def get(self, request, format=None):
        symbol = request.query_params.get('symbol')
        address = request.query_params.get('address')

        if not address or not symbol:
            return Response({"error": "Currency or address were not entered"}, status=status.HTTP_400_BAD_REQUEST)
        if symbol == "BTC":
            balance = get_btc_balance(address)
        elif symbol == "ETH":
            balance = get_eth_balance(address)
        elif symbol == "SOL":
            balance = get_solana_balance(address)
        else:
            return Response({"error": f"Unsupported symbol entered: {symbol}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(balance, status=status.HTTP_200_OK)
