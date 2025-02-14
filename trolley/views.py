from django.shortcuts import render, get_object_or_404, redirect
from .trolley import Trolley
from shop.models import Product, Size
from django.http import JsonResponse
from django.contrib import messages
import shop.urls
from review.models import Review

# Create your views here.
def trolley_summary(request):
	# get trolley
	reviews = Review.objects.filter(is_active=True)
	trolley = Trolley(request)
	trolley_products = trolley.get_prods
	quantities = trolley.get_quants
	product_sizes = trolley.get_prods_sizes
	sizes = trolley.get_sizes
	totals = trolley.trolley_total()
	return render(request, 'trolley_summary.html', {'reviews': reviews, 'product_sizes':product_sizes, 'trolley_products':trolley_products, 'quantities':quantities, 'sizes':sizes, 'totals':totals, 'current_trolley': trolley.trolley})


def trolley_add(request):
	# get the trolley
	trolley = Trolley(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty')) 
		product_size = str(request.POST.get('product_size'))
		# look up product in DB
		product = get_object_or_404(Product, id=product_id)
		if not product.is_sold_out:
			# save to session
			trolley.add(product=product, quantity=product_qty, size=product_size)

			# get trolley quantity
			trolley_quantity = trolley.__len__()
			trolley_sizes = trolley.get_prods_sizes()

			# return response
			# response = JsonResponse({'Product Name: ': product.name})
			response = JsonResponse({'qty': trolley_quantity, 'sizes': trolley_sizes})
			messages.success(request, ('This was added to your trolley.'))
			return response
		else:
			trolley_quantity = trolley.__len__()

			# return response
			# response = JsonResponse({'Product Name: ': product.name})
			response = JsonResponse({'qty': trolley_quantity})
			messages.error(request, "Sorry that one isn't available at the moment.")
			return response


def trolley_delete(request):
	trolley = Trolley(request)
	if request.POST.get('action') == 'post':
		#get stuff
		product_id = int(request.POST.get('product_id'))
		# call delete function
		trolley.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		messages.success(request, 'Item removed from shopping trolley.')
		return response
		# return redirect('trolley_summary')


def trolley_update(request):
	trolley = Trolley(request)
	if request.POST.get('action') == 'post':
		#get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))
		product_size = str(request.POST.get('product_size'))

		trolley.update(product=product_id, quantity=product_qty, size=product_size)

		response = JsonResponse({'qty': product_qty, 'sizes': product_size})
		messages.success(request, 'Your trolley has been updated.')
		return response
		# return redirect('trolley_summary')