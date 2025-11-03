from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.dia_api import get_price

curryncies = ["BTC", "ETH", "USDT", "XRP", "BNB", "SOL", "USDC", "stETH", "TRX", "DOGE", "ADA", "WBTC", "HYPE", "LINK", "BCH"]

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