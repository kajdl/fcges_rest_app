from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Stock, Order
from django.db.models import Sum


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')  
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False} 
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    stock_id = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        exclude = ('user',)
        read_only_fields = ('timestamp',)
    
    def validate(self, data):
        user = self.context['request'].user
        stock_id = data.get('stock_id')
        order_type = data.get('order_type')
        quantity = data.get('quantity')

        if order_type == Order.SELL:
            try:
                stock = Stock.objects.get(id=stock_id)
            except Stock.DoesNotExist:
                raise serializers.ValidationError("Stock does not exist")
            
            total_bought = Order.objects.filter(
                user=user,
                stock=stock,
                order_type=Order.BUY
            ).aggregate(total=Sum('quantity'))['total'] or 0

            total_sold = Order.objects.filter(
                user=user,
                stock=stock,
                order_type=Order.SELL
            ).aggregate(total=Sum('quantity'))['total'] or 0

            available_quantity = total_bought - total_sold

            if quantity > available_quantity:
                raise serializers.ValidationError(
                    f"You don't have enough stocks to sell. You own {available_quantity} shares."
                )
        
        return data
    
    def create(self, validated_data): 
        validated_data['user'] = self.context['request'].user
        validated_data['stock'] = Stock.objects.get(id=validated_data.pop('stock_id'))
        return super().create(validated_data)
    
class PortfolioSerializer(serializers.Serializer):
    stock = StockSerializer()
    total_quantity = serializers.IntegerField()
    total_investment = serializers.DecimalField(max_digits=12, decimal_places=2)
    current_value = serializers.DecimalField(max_digits=12, decimal_places=2)