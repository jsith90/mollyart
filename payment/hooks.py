from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import time
from .models import Order
from .views import handle_payment_intent_succeeded, send_email


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
	# add ten second pause for paypal to send ipn data
	time.sleep(10)
	# grab info that paypal sends
	paypal_obj = sender
	# grab the invoice
	my_Invoice = str(paypal_obj.invoice)
	my_payerId = str(paypal_obj.payer_id)
	# match paypal invoice to model order invoice
	my_Order = Order.objects.get(invoice=my_Invoice)
	# record tha the order was paid
	my_Order.payment_method = 'paypal' 
	my_Order.paid = True
	# save order
	my_Order.save()
	# print(paypal_obj)
	# print(f'Amount Paid: {paypal_obj.mc_gross}')
	handle_payment_intent_succeeded(my_Order)
	send_email(my_Order)