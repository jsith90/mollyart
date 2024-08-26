from django.shortcuts import render, redirect
from trolley.trolley import Trolley
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from shop.models import Product
import datetime


def orders(request, pk):
	if request.user.is_superuser:
		# get the order
		order = Order.objects.get(id=pk)
		# get the order item
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# check if true or false
			if status == "true":
				# get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)

			messages.success(request, "Shipping Status Updated")
			return redirect('index')

		return render(request, 'payment/orders.html', {'order':order, 'items':items})
	else:
		messages.success(request, 'Access Denied.')
		return redirect('index')


def not_shipped_dash(request):
	if request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# get order
			order = Order.objects.filter(id=num)
			# Update the status
			now = datetime.datetime.now()
			order.update(shipped=True, date_shipped=now)

			messages.success(request, "Shipping Status Updated")
			return redirect('index')
			
		return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
	else:
		messages.success(request, 'Access Denied.')
		return redirect('index')
	

def shipped_dash(request):
	if request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# get order
			order = Order.objects.filter(id=num)
			# Update the status
			now = datetime.datetime.now()
			order.update(shipped=False)

			messages.success(request, "Shipping Status Updated")
			return redirect('index')

		return render(request, 'payment/shipped_dash.html', {'orders':orders})
	else:
		messages.success(request, 'Access Denied.')
		return redirect('index')

def process_order(request):
	# get trolley
	trolley = Trolley(request)
	trolley_products = trolley.get_prods
	quantities = trolley.get_quants
	totals = trolley.trolley_total()
	if request.POST:
		# getting billing info from the last page
		payment_form = PaymentForm(request.POST or None)
		# get shipping session data
		my_shipping = request.session.get('my_shipping')
		# gather order info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		amount_paid = totals
		# Create shipping address from shipping info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_region']}\n{my_shipping['shipping_postcode']}\n{my_shipping['shipping_country']}"
		# Create an orde
		# not logged in
		# create order
		create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
		create_order.save()
		# add order items
		order_id = create_order.pk
		# get product stuff
		for product in trolley_products():
			# get product id
			product_id = product.id
			# get product price
			if product.is_sale:
				price = product.sale_price
			else:
				price = product.price
			# get quantity
			for key,value in quantities().items():
				if int(key) == product.id:
					# create order itemv
					create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price,)
					create_order_item.save()
					# Update the quantity of the product in the Product app
					product_obj = Product.objects.get(id=product_id)
					product_obj.quantity -= value  # Subtract the purchased quantity
					if product_obj.quantity == 0:
						product_obj.is_sold_out = True
						product_obj.is_sale = False 
					product_obj.save()  # Save the updated product

			# delete our trolley
			for key in list(request.session.keys()):
				if key == 'session_key':
					del request.session[key]
					
			messages.success(request, 'Order Placed.')
			return redirect('index')
	else:
		messages.error(request, 'Access Denied.')
		return redirect('index')


def billing_info(request):
	if request.POST:

		# get trolley
		trolley = Trolley(request)
		trolley_products = trolley.get_prods
		quantities = trolley.get_quants
		totals = trolley.trolley_total()

		# create a session with shipping info
		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping
		# Not logged in
		billing_form = PaymentForm()
		return render(request, 'payment/billing_info.html', {'trolley_products':trolley_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'billing_form': billing_form})


		shipping_info = request.POST
		return render(request, 'payment/billing_info.html', {'trolley_products':trolley_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})

	else: 
		messages.error(request, 'Access Denied.')
		return redirect('index')
	

def checkout(request):
	# get trolley
	trolley = Trolley(request)
	trolley_products = trolley.get_prods
	quantities = trolley.get_quants
	totals = trolley.trolley_total()
	# Check out as guest
	shipping_form = ShippingForm(request.POST or None)
	return render(request, 'payment/checkout.html', {'trolley_products':trolley_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})

def payment_success(request):
	return render(request, 'payment/payment_success.html', {})
