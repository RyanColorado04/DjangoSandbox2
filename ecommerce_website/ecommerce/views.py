from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem

# Displays a list of all products to the user
def product_list(request):
    products = Product.objects.all()  # Retrieve all products from the database
    # Render the product list template with the products context
    return render(request, 'ecommerce/product_list.html', {'products': products})

# Displays the details of a single product
def product_detail(request, product_id):
    # Get the Product object with the given product_id or return a 404 error if not found
    product = get_object_or_404(Product, pk=product_id)
    # Render the product detail template for the given product
    return render(request, 'ecommerce/product_detail.html', {'product': product})

# Adds a product to the user's cart
@login_required  # Ensure that only logged-in users can add to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)  # Get the product or return 404
    # Retrieve or create an Order object for the user that is not yet ordered (in the cart)
    order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
    # Retrieve or create an OrderItem for the product in the order
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1  # Increment the quantity of the product in the cart
    order_item.save()  # Save the changes to the order item
    return redirect('product_list')  # Redirect to the product list page

# View the cart and its items
@login_required  # User must be logged in to view their cart
def view_cart(request):
    order = Order.objects.get(user=request.user, is_ordered=False)  # Get the user's cart
    order_items = order.orderitem_set.all()  # Retrieve all items from the user's cart
    # Render the view cart template with the order and order_items context
    return render(request, 'ecommerce/view_cart.html', {'order': order, 'order_items': order_items})

# Handles the checkout process
@login_required  # Only logged-in users should be able to checkout
def checkout(request):
    order = Order.objects.get(user=request.user, is_ordered=False)  # Get the user's cart
    order.is_ordered = True  # Set the order status to True as it is now ordered
    order.save()  # Save the order to mark it as completed
    # Render the checkout template showing the order summary and a thank you message
    return render(request, 'ecommerce/checkout.html', {'order': order})
