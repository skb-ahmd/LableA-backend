from rest_framework import serializers
from .models import Cart, CartItem, Product

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model=Product
		fields='__all__'


class CartItemSerializer(serializers.ModelSerializer):
	product = ProductSerializer(read_only=True)
	class Meta:
		model = CartItem
		fields = ['id', 'cart', 'product', 'quantity']

	def create(self, validated_data):
		product_id = self.initial_data.get('product') # Get product ID from request data
		try:
			product = Product.objects.get(pk=product_id)
		except Product.DoesNotExist:
			raise serializers.ValidationError("Invalid product ID")
		validated_data['product'] = product
		return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
	cartitem_set = CartItemSerializer(many=True, read_only=True)

	class Meta:
		model = Cart
		fields = ['id', 'user', 'created_at', 'updated_at', 'cartitem_set']


from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id',  'delivery_time', 'cart_items', 'created_at']