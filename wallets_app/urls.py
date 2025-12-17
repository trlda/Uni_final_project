from django.urls import path
from .views import WalletListView, WalletConnectView, WalletDisconnectView

urlpatterns = [
    path("", WalletListView.as_view()),
    path("connect/", WalletConnectView.as_view()),
    path("disconnect/<str:symbol>/", WalletDisconnectView.as_view()),
]
