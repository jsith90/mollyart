from django.shortcuts import render, get_object_or_404
from .trolley import Trolley
from shop.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def trolley_summary(request):
	# get trolley
	trolley = Trolley(request)
	trolley_products = trolley.get_prods
	quantities = trolley.get_quants
	totals = trolley.trolley_total()
	return render(request, 'trolley_summary.html', {'trolley_products':trolley_products, 'quantities':quantities, 'totals':totals})


def trolley_add(request):
	# get the trolley
	trolley = Trolley(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty')) 
		# look up product in DB
		product = get_object_or_404(Product, id=product_id)
		# save to session
		trolley.add(product=product, quantity=product_qty)

		# get trolley quantity
		trolley_quantity = trolley.__len__()

		# return response
		# response = JsonResponse({'Product Name: ': product.name})
		response = JsonResponse({'qty': trolley_quantity})
		messages.success(request, ('Product added to trolley.'))
		return response


def trolley_delete(request):
	trolley = Trolley(request)
	if request.POST.get('action') == 'post':
		#get stuff
		product_id = int(request.POST.get('product_id'))
		# call delete function
		trolley.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		messages.success(request, ('Item removed from shopping trolley.'))
		return response
		# return redirect('trolley_summary')


def trolley_update(request):
	trolley = Trolley(request)
	if request.POST.get('action') == 'post':
		#get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		trolley.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		messages.success(request, ('Your trolley has been updated.'))
		return response
		# return redirect('trolley_summary')