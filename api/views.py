from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.db.models import F, Sum
from .models import Stock, Order
from .serializers import UserSerializer, StockSerializer, OrderSerializer,  PortfolioSerializer


class UserCreateView(generics.CreateAPIView):

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'created': created
        })
    
class StockListView(generics.ListAPIView):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Stock.objects.all()

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('stock')
    
class PortfolioItem:
    def __init__(self, stock, total_quantity, total_investment, current_value):
        self.stock = stock
        self.total_quantity = total_quantity
        self.total_investment = total_investment
        self.current_value = current_value

class PortfolioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_portfolio_data(self, user, stock=None):
        orders = Order.objects.filter(user=user)
        
        if stock:
            orders = orders.filter(stock=stock)
            if not orders.exists():
                return None
        
        stock_ids = orders.values('stock').distinct()
        stocks = [stock] if stock else Stock.objects.filter(id__in=stock_ids)
        
        portfolio = []
        
        for s in stocks:
            stock_orders = orders.filter(stock=s)
            
            bought = stock_orders.filter(order_type=Order.BUY).aggregate(
                total=Sum(F('quantity') * F('price')),
                qty=Sum('quantity')
            )
            
            sold = stock_orders.filter(order_type=Order.SELL).aggregate(
                total=Sum(F('quantity') * F('price')),
                qty=Sum('quantity')
            )
            
            net_qty = (bought['qty'] or 0) - (sold['qty'] or 0)
            
            if net_qty <= 0 and not stock:
                continue
                
            portfolio.append(
                PortfolioItem(
                    stock=s,
                    total_quantity=net_qty,
                    total_investment=(bought['total'] or 0) - (sold['total'] or 0),
                    current_value=net_qty * s.current_price
                )
            )
        
        return portfolio or None
    
    def get(self, request, stock_id=None):
        user = request.user
        stock = None

        if stock_id:
            try:
                stock = Stock.objects.get(id=stock_id.upper())
            except Stock.DoesNotExist:
                return Response(
                    {'error': 'Stock not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

        portfolio = self.get_portfolio_data(user, stock)

        if stock and not portfolio:
            return Response(
                {'error': 'No holdings for this stock'},
                status=status.HTTP_404_NOT_FOUND
            )

        if stock_id:
            return Response(PortfolioSerializer(portfolio[0]).data)

        total_value = sum(item.current_value for item in portfolio)
        return Response({
            'portfolio': PortfolioSerializer(portfolio, many=True).data,
            'total_value': total_value
        })