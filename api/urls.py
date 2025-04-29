from django.urls import path
from .views import UserCreateView, CustomAuthToken, StockListView, OrderCreateView, OrderListView, PortfolioView

urlpatterns = [
    path('signup/', UserCreateView.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('stocks/', StockListView.as_view()),
    path('orders/', OrderCreateView.as_view()),
    path('orders/list/', OrderListView.as_view()),
    path('portfolio/', PortfolioView.as_view()),
    path('portfolio/<str:stock_id>/', PortfolioView.as_view()),
]