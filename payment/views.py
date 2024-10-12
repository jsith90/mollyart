from django.shortcuts import render, redirect
from trolley.trolley import Trolley
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from shop.models import Product, Size
import datetime
# paypal stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid #unique user id for duplicate orders
import stripe
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import logging
import time
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

def orders(request, pk):
	if request.user.is_superuser:
		# get the order
		order = Order.objects.get(id=pk)
		# get the order item
		items = OrderItem.objects.filter(order=order)

		if request.POST:
			status = request.POST['shipping_status']
			# check if true or false
			if status == "true":
				# Update the status
				now = datetime.datetime.now()
				order.shipped = True
				order.date_shipped = now
				order.save()
				order_shipped_email(request, order)
			else:
				# get the order
				order.shipped = False
				# Update the status
				order.save()

			messages.success(request, "Shipping Status Updated.")
			return redirect('not_shipped_dash')

		return render(request, 'payment/orders.html', {'order':order, 'items':items})
	else:
		messages.error(request, "Not authorised to do that bud.")
		return redirect('index')


def not_shipped_dash(request):
	if request.user.is_superuser:
		orders = Order.objects.filter(shipped=False, paid=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# get order
			order = Order.objects.get(id=num)
			# Update the status
			now = datetime.datetime.now()
			order.shipped=True
			order.date_shipped=now
			order.save()
			order_shipped_email(request, order)
			messages.success(request, "Shipping Status Updated.")
			return redirect('not_shipped_dash')
			
		return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
	else:
		messages.error(request, "Not authorised to do that bud.")
		return redirect('index')

def order_shipped_email(request, order):
	items = OrderItem.objects.filter(order=order)
	order_email = order.email
	is_valid_email = True
	try:
		validate_email(order_email)
	except ValidationError:
		is_valid_email = False
	if is_valid_email:
		subject = "Your order has been shipped!"
		from_email = "j.sinclairthomson@gmail.com"
		to_email = [order_email] 
		html_template = get_template('payment/shipped_email.html')
		html_content = html_template.render({'order': order, 'items': items})
		email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
		email_message.attach_alternative(html_content, "text/html")
		email_message.send()
	else:
		messages.error(request, 'The email was invalid and and a shipping confirmation could not be sent.')
		return redirect('not_shipped_dash')


def shipped_dash(request):
	if request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# get order
			order = Order.objects.get(id=num)
			# Update the status
			now = datetime.datetime.now()
			order.shipped = False
			order.date_shipped = None
			order.save()

			messages.success(request, "Shipping Status Updated.")
			return redirect('shipped_dash')

		return render(request, 'payment/shipped_dash.html', {'orders':orders})
	else:
		messages.error(request, "Not authorised to do that bud.")
		return redirect('index')


def calculate_order_amount(items):
	total_amount = 0
	for item in items:
		product_id = item['id']
		quantity = item['quantity']
		product = Product.objects.get(id=product_id)
		# Determine the price to use
		if product.is_sale:
			price = product.sale_price
		else:
			price = product.price
		# Multiply price by quantity and add to the total amount
		total_amount += price * quantity
		# Return the total amount in the smallest currency unit (e.g., pence for GBP)
	return int(total_amount * 100)  # Convert to pence if using GBP


def billing_info(request):
	# get trolley
	trolley = Trolley(request)
	trolley_products = trolley.get_prods
	product_sizes = trolley.get_product_sizes()
	sizes = trolley.get_sizes()
	quantities = trolley.get_quants
	current_trolley = trolley.trolley
	totals = trolley.trolley_total()
	if request.POST:
		# create a session with shipping info
		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping
		# gather order info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		amount_paid = totals
		# Create shipping address from shipping info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_region']}\n{my_shipping['shipping_postcode']}\n{my_shipping['shipping_country']}"

		# create payment intent in stripe
		items = [{'id': product.id, 'quantity': quantities()[str(product.id)]} for product in trolley_products()]
		intent = stripe.PaymentIntent.create(
			amount=calculate_order_amount(items),
			currency='gbp',
			automatic_payment_methods={
				'enabled': True,
			},
		)

		# paypal form dictionary and stuff
		host = request.get_host()
		# create invoice number
		my_Invoice = str(uuid.uuid4())

		# create order
		paypal_dict = {
			'business': settings.PAYPAL_RECEIVER_EMAIL,
			'amount': totals,
			'item_name': "Molly's Art Order",
			'no_shipping': '2',
			'invoice': my_Invoice,
			'currency_code': 'GBP',
			'notify_url': 'https://{}{}'.format(host, reverse('paypal-ipn')),
			'return_url': 'https://{}{}'.format(host, reverse('payment_success')),
			'cancel_return': 'https://{}{}'.format(host, reverse('payment_failed')),
		}

		# create paypal button
		paypal_form = PayPalPaymentsForm(initial=paypal_dict)
		
		# create an order 
		create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid, payment_intent_id=intent.id, invoice=my_Invoice)
		create_order.save() 
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
			if not product.is_size:
				for key,value in quantities().items():
					if int(key) == product.id:
						# create order itemv
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price,)
						create_order_item.save()
						print(create_order_item)
			else:
				sizes_list = []
				for size in sizes:
					for key,value in current_trolley.items():
						if str(key).startswith(str(product.id)):
							print(type(key), key, type(value), value)
							if value['size'] == size.size:
								size_quantity = f"{size.size}: {str(value['quantity'])}"
								sizes_list.append(size_quantity)
								print('This is:', size_quantity)
				sizes_string = ', '.join(sizes_list)
				create_order_item = OrderItem(is_size=True, order_id=order_id, product_id=product_id, size=sizes_string, price=price,)
				create_order_item.save()
				print(create_order_item)
		return render(request, 'payment/billing_info.html', { 'current_trolley':current_trolley, 'sizes':sizes, 'client_secret':intent.client_secret, 'STRIPE_PUBLIC_KEY':settings.STRIPE_PUBLIC_KEY, 'paypal_form':paypal_form, 'trolley_products':trolley_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST })


		# shipping_info = request.POST
		# return render(request, 'payment/billing_info.html', {'trolley_products':trolley_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form})

	else: 
		messages.error(request, 'Access Denied.')
		return redirect('index')
	

def checkout(request):
    # Get trolley
    trolley = Trolley(request)
    trolley_products = trolley.get_prods()  # List of products in the trolley
    sizes = trolley.get_sizes()  # List of sizes in the trolley
    quantities = trolley.get_quants()  # Quantities of products
    totals = trolley.trolley_total()  # Trolley total price

    # Handle sold-out products (those not size-specific)
    sold_out_ids = [product.id for product in trolley_products if not product.is_size and product.is_sold_out]
    sold_out_size_ids = [size.id for size in sizes if size.is_sold_out]
    if sold_out_ids:
        for product_id in sold_out_ids:
            product = Product.objects.get(id=product_id)  # Get the product instance
            messages.error(request, f'Sorry, {product.name} is sold out and has been removed from your trolley.')
            # Remove sold-out products from the trolley
            trolley.delete(product=product_id)
            return redirect('trolley_summary')
    # Handle sold-out sizes
    if sold_out_size_ids:
    	to_delete= []
    	for size in sizes:
            if size.id in sold_out_size_ids:
                product = size.product  # Get the product associated with the size
                current_trolley = trolley.trolley
                for key, item in current_trolley.items():
                    if str(product.id) in key and item['size'] == size.size:
                        messages.error(request, f'Sorry, {product.name} in size {size.size} is sold out and has been removed from your trolley.')
                        to_delete.append(product.id)
    	for product_id in to_delete:
    		trolley.delete(product=product_id)

    		return redirect('trolley_summary')

    shipping_form = ShippingForm(request.POST or None)
    return render(request, 'payment/checkout.html', {'current_trolley': trolley.trolley, 'sizes': sizes, 'trolley_products': trolley_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form })


@csrf_exempt
def stripe_webhook(request):

	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, endpoint_secret
		)
	except ValueError as e:
	# Invalid payload
		print('Error parsing payload: {}'.format(str(e)))
		logger.error("Error handling webhook: %s", str(e))
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		logger.error("Error handling webhook: %s", str(e))
		print('Error verifying webhook signature: {}'.format(str(e)))
		return HttpResponse(status=400)

	# handle event
	if event['type'] == 'payment_intent.created':
		# Handle the payment intent creation
		logger.info("Payment intent created: %s", event['data']['object'])
		# Process the payment intent as needed
		payment_intent = event['data']['object']  # This is the payment intent object
		payment_intent_id = payment_intent['id']  # Correctly retrieve the payment intent ID
		return HttpResponse({'status': 'success'}, status=200)
	elif event['type'] == 'charge.succeeded':
		# Handle the payment intent creation
		logger.info("Charge succeeded: %s", event['data']['object'])
		# Process the payment intent as needed
		return HttpResponse({'status': 'success'}, status=200)
	elif event['type'] == 'charge.updated':
		# Handle the payment intent creation
		logger.info("Charge updated: %s", event['data']['object'])
		# Process the payment intent as needed
		return HttpResponse({'status': 'success'}, status=200)
	elif event['type'] == 'payment_intent.succeeded':
		payment_intent_id = event['data']['object']['id']
		my_order = Order.objects.get(payment_intent_id=payment_intent_id)
		my_order.payment_method = 'stripe'
		my_order.paid = True
		my_order.save()
		handle_payment_intent_succeeded(my_order)
		send_email(my_order)
		purchase_notification_email(my_order)
		return HttpResponse({'status': 'success'}, status=200)
	else:
		logger.warning(f'Unhandled event type: {event["type"]}')
		# Process the payment intent as needed

import time

def handle_payment_intent_succeeded(order):
    time.sleep(5)
    # Get order items associated with the order
    items = OrderItem.objects.filter(order=order)
    if order.paid:
        for item in items:
            print(f"Processing item ID: {item.id}, is_size: {item.is_size}, size: {item.size}")
            product = Product.objects.get(id=item.product_id)  # Get the product by ID
            # If the item has sizes, parse the size field
            if item.is_size == True:
                # Split the sizes string (e.g., 'size: Small: 1, size: Medium: 2')
                size_entries = item.size.split(', ')  # Split by comma and space

                for size_entry in size_entries:
                    # Example size_entry: 'size: Small: 1'
                    size_info = size_entry.split(': ')
                    size_name = size_info[0].strip()
                    size_quantity = int(size_info[1].strip())  # 1

                    # Update the corresponding ProductSize entry
                    product_size = Size.objects.get(product=product, size=size_name)
                    product_size.quantity -= size_quantity  # Subtract the quantity for the size
                    
                    # If the quantity is zero, mark as sold out for this size
                    if product_size.quantity <= 0:
                        product_size.is_sold_out = True  # Ensure it doesn't go negative

                    product_size.save()  # Save the updated size quantity

            else:
                # No size handling, just update the product quantity
                product.quantity -= item.quantity  # Subtract the purchased quantity

                # If the product quantity is zero, mark as sold out
                if product.quantity <= 0:
                    product.is_sold_out = True
                    product.is_sale = False

                product.save()  # Save the updated product
 

def send_email(order):
	items = OrderItem.objects.filter(order=order)
	order_email = order.email
	subject = "Your order has been placed!"
	from_email = "j.sinclairthomson@gmail.com"
	to_email = [order_email] 
	html_template = get_template('payment/order_email.html')
	html_content = html_template.render({'order': order, 'items': items})
	email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
	email_message.attach_alternative(html_content, "text/html")
	email_message.send()


def purchase_notification_email(order):
	items = OrderItem.objects.filter(order=order)
	subject = "You have a new customer!"
	from_email = "j.sinclairthomson@gmail.com"
	to_email = ["j.sinclairthomson@gmail.com"] 
	html_template = get_template('payment/notification.html')
	html_content = html_template.render({'order': order, 'items': items})
	email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
	email_message.attach_alternative(html_content, "text/html")
	email_message.send()

	
def payment_success(request):
	time.sleep(10)
	# Get the payerID from the request
	payer_id = request.GET.get('payer_id')
    # get the order
	order = Order.objects.filter(payer_id=payer_id).order_by('-date_ordered').first()
	# get the order item
	items = OrderItem.objects.filter(order=order)
	# delete browser cart
	# get trolley
	trolley = Trolley(request)
	trolley_products = trolley.get_prods
	quantities = trolley.get_quants
	totals = trolley.trolley_total()
	# Update the quantity of the product in the Product app
	# product_obj = Product.objects.get(all)
	# product_obj.quantity -= value  # Subtract the purchased quantity
	# if product_obj.quantity == 0:
	# 	product_obj.is_sold_out = True
	# 	product_obj.is_sale = False 
	# 	product_obj.save()  # Save the updated product
	# if order.paid:
	# 	for item in items:
	# 		product = Product.objects.get(id=item.product_id)  # Get the product by ID
	# 		product.quantity -= item.quantity  # Subtract the purchased quantity
	# 		# If quantity is zero, mark as sold out
	# 		if product.quantity <= 0:
	# 			product.is_sold_out = True
	# 			product.is_sale = False 

	# 		product.save() 
	 	# delete our trolley
	for key in list(request.session.keys()):
		if key == 'session_key':
			del request.session[key]

	return render(request, 'payment/payment_success.html', {'order':order, 'items':items })


def payment_failed(request):
	return render(request, 'payment/payment_failed.html', {})