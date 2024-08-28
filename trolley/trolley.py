from shop.models import Product

class Trolley():
	def __init__(self, request):
		self.session = request.session
		# Get request
		self.request = request
		# get current session key if it exists
		trolley = self.session.get('session_key')
		if 'session_key' not in request.session:
			trolley = self.session['session_key'] = {}


		# make sure trolley is available on all pages of site
		self.trolley = trolley

	def db_add(self, product, quantity):
		product_id = str(product)
		product_qty = str(quantity)
		# logic
		if product_id in self.trolley:
			pass
		else:
			# self.trolley[product_id] = {'price': str(product.price)}
			self.trolley[product_id] = int(product_qty)
		
		self.session.modified = True
	


	def add(self, product, quantity):
		product_id = str(product.id)
		product_qty = str(quantity)
		# logic
		if product_id in self.trolley:
			pass
		else:
			# self.trolley[product_id] = {'price': str(product.price)}
			self.trolley[product_id] = int(product_qty)
		
		self.session.modified = True


	def trolley_total(self):
		# get product ids
		product_ids = self.trolley.keys()
		print(product_ids)
		# look up keys in our products database model
		products = Product.objects.filter(id__in=product_ids)
		print(f'this is {product_ids}') 
		# get quantities
		quantities = self.trolley
		# start counting at 0
		total = 0
		for key, value in quantities.items():
			key = int(key)
			for product in products:
				if product.id == key:
					if product.is_sale:
						total = total + (product.sale_price * value)
					else:
						total = total + (product.price * value)
		return total



	def __len__(self):
		return sum(self.trolley.values())

	def get_prods(self):
		# get ids from trolley
		product_ids = self.trolley.keys()
		# use ids to look up products in db model
		products = Product.objects.filter(id__in=product_ids)
		return products

	def get_quants(self):
		quantities = self.trolley
		return quantities

	def update(self, product, quantity):
		product_id = str(product)
		product_qty = int(quantity)
		ourtrolley = self.trolley
		ourtrolley[product_id] = product_qty
		self.session.modified = True
		thing = self.trolley
		return thing

	def delete(self, product):
		product_id = str(product)
		# delete from dictionary
		if product_id in self.trolley:
			del self.trolley[product_id]

		self.session.modified = True 

