from django.urls import path, include
from .router import WalletRouter


app_name = 'Wallets'

wallet_router = WalletRouter()

urlpatterns = [
    path('wallets/', include(wallet_router.get_urls())),
]
