from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet
from .serializers import WalletSerializer


class WalletListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)


class WalletConnectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        symbol = request.data.get("symbol")
        address = request.data.get("address")

        if not symbol or not address:
            return Response(
                {"error": "symbol and address required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        wallet, created = Wallet.objects.get_or_create(
            user=request.user,
            symbol=symbol,
            defaults={"address": address},
        )

        if not created:
            wallet.address = address
            wallet.save()

        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WalletDisconnectView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, symbol):
        wallet = Wallet.objects.filter(
            user=request.user,
            symbol=symbol
        ).first()

        if not wallet:
            return Response(
                {"error": "Wallet not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        wallet.delete()
        return Response(
            {"message": f"{symbol} wallet disconnected"},
            status=status.HTTP_200_OK
        )
