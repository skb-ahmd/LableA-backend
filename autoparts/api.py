from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem, Order, Product
from .serializers import CartItemSerializer, CartSerializer, OrderSerializer, ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):


	# cart = Cart.objects.get(id=4)
	# cart_items = cart.cartitem_set.all()
	# print(cart_items)        


	queryset = Cart.objects.all()
	serializer_class = CartSerializer

	def create(self, request, *args, **kwargs):
		user_id = request.data.get('user')
		if not user_id:
			return Response({"error": "User ID is required"}, status=400)


		return super().create(request, *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		print("Destroy method called")
		return super().destroy(request, *args, **kwargs)


# class CartItemViewSet(viewsets.ModelViewSet):
# 	queryset = CartItem.objects.all()
# 	serializer_class = CartItemSerializer

# 	def create(self, request, *args, **kwargs):
# 		cart_id = int(request.data.get('cart'))
# 		product_id = request.data.get('product')
# 		quantity = int(request.data.get('quantity', 1))
# 		print(f"Cart ID: {cart_id}, Product ID: {product_id}, Quantity: {quantity}")

# 		if not product_id:
# 			return Response({"error": "Product ID is required"}, status=400)
		
# 		try:
# 			product = Product.objects.get(pk=product_id)
# 			available_quantity = product.available_quantity
# 			# print(available_quantity)

# 			if quantity > available_quantity:
# 				return Response({"error": "Requested quantity exceeds available quantity"}, status=400)
# 		except Product.DoesNotExist:
# 			return Response({"error": "Invalid product ID"}, status=400)

# 		existing_cart_item = CartItem.objects.filter(cart=cart_id, product=product_id).first()

# 		if existing_cart_item:
# 			print('there')
# 			existing_cart_item.quantity += quantity
# 			existing_cart_item.save()
# 			serializer = self.get_serializer(existing_cart_item)
# 			return Response(serializer.data)
# 		else:
# 			# print('here')
			
# 			serializer = self.get_serializer(data=request.data)
# 			print(f"Serializer data: {serializer.initial_data}")
# 			# print(serializer.is_valid)
# 			if not serializer.is_valid(raise_exception=True):
# 				print('error')
# 				print(serializer.errors)
# 			serializer.is_valid(raise_exception=True)
# 			self.perform_create(serializer)
# 			headers = self.get_success_headers(serializer.data)
# 			return Response(serializer.data, status=201, headers=headers)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        cart_id = int(request.data.get('cart'))
        product_id = int(request.data.get('product'))
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        try:
            product = Product.objects.get(pk=product_id)
            available_quantity = product.available_quantity

            if quantity > available_quantity:
                return Response({"error": "Requested quantity exceeds available quantity"}, status=400)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product ID"}, status=400)

        existing_cart_item = CartItem.objects.filter(cart=cart_id, product=product_id).first()

        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
            serializer = self.get_serializer(existing_cart_item)
            return Response(serializer.data)
        else:
            cart_item_data = {
                'cart': cart_id,
                'product': product_id,  # Only pass the product ID here
                'quantity': quantity
            }
            serializer = self.get_serializer(data=cart_item_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)

   
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def process_order(self, request):
        # Extract necessary parameters from the request data
        cart_id = request.data.get('cart_id')
        delivery_time = request.data.get('delivery_time')

        # Check if the required parameters are provided
        if not cart_id or not delivery_time:
            return Response({'error': 'Both cart_id and delivery_time are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            # Retrieve the cart and cart items
            cart = Cart.objects.get(id=cart_id)
            cart_items = cart.cartitem_set.all()

            # Check if there are items in the cart
            if not cart_items.exists():
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

            print(cart_items)
            # Check if the requested quantity is available for each item
            for cart_item in cart_items:
                print(cart_item.product)
                if cart_item.quantity > cart_item.product.available_quantity:
                    return Response({'error': f'Requested quantity for {cart_item.product.name} exceeds available quantity'},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Create a new order
            order = Order.objects.create(
                delivery_time=delivery_time
            )

            # Reduce the quantities and associate cart items with the order
            for cart_item in cart_items:
                cart_item.product.available_quantity -= cart_item.quantity
                cart_item.product.save()
                order.cart_items.add(cart_item)

            # Save the order
            order.save()

            # Clear the cart
            cart.cartitem_set.all().delete()

            # Return a response with the new order details
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)