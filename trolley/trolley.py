from shop.models import Product, Size
from decimal import Decimal, ROUND_HALF_UP


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
	

	def add(self, product, quantity, size=None):
	    product_id = str(product.id)
	    product_qty = str(quantity)
	    product_size = str(size) if size else None

	    # Ensure size is part of the key to differentiate between sizes
	    if product_size:
	        key = f"{product_id}_{product_size}"
	    else:
	        key = product_id

	    # Logic
	    if key in self.trolley:
	        pass
	    else:
	        self.trolley[key] = {
	            'quantity': int(product_qty),
	            'size': product_size,
	        }

	    self.session.modified = True


	def trolley_total(self):
	    product_keys = self.trolley.keys()
	    product_ids = [key.split('_')[0] for key in product_keys]  # Extract product ids
	    products = Product.objects.filter(id__in=product_ids)
	    total = 0

	    for key, value in self.trolley.items():
	        product_id = int(key.split('_')[0])  # Get product id
	        size = key.split('_')[1] if '_' in key else None  # Get size if available
	        quantity = value['quantity'] if isinstance(value, dict) else value  # Get the quantity

	        for product in products:
	            if product.id == product_id:
	                if product.is_sale:
	                    total += product.sale_price * quantity
	                else:
	                    total += product.price * quantity

	    return total


	def trolley_postage_packaging(self):
		product_keys = self.trolley.keys()
		product_ids = [key.split('_')[0] for key in product_keys]
		products = Product.objects.filter(id__in=product_ids)
		weight_total = 0
		postage = 0

		for key, value in self.trolley.items():
			product_id = int(key.split('_')[0])
			size = key.split('_')[1] if '_' in key else None
			quantity = value['quantity'] if isinstance(value, dict) else value

			for product in products:
				if product.id == product_id:
					if product.weight:
						weight_total += product.weight * quantity


		if weight_total <= 1:
			postage = Decimal('3.50')
		elif weight_total <= 4:
			postage = Decimal('4.50')
		elif weight_total <= 10:
			postage = Decimal('10.50')
		elif weight_total <= 20:
			postage = Decimal('21.00')
		elif weight_total <= 50:
			postage = Decimal('40.00')
		elif weight_total <= 100:
			postage = Decimal('80.00') 
		return postage


	def absolute_total(self):
		total = self.trolley_total()
		postage = self.trolley_postage_packaging()

		absolute_total = total + postage

		return absolute_total


	def __len__(self):
	    # Sum the quantities from the dictionaries in self.trolley
	    return sum(item if isinstance(item, int) else item['quantity'] for item in self.trolley.values())


	def get_prods(self):
	    # Get ids from trolley (assuming keys are formatted like '5_Small')
	    product_ids = [int(key.split('_')[0]) for key in self.trolley.keys()]
	    # Use ids to look up products in DB
	    products = Product.objects.filter(id__in=product_ids)
	    return products


	def get_sizes(self):
	    product_ids = [int(key.split('_')[0]) for key in self.trolley.keys()] # Extract product IDs
	    sizes = Size.objects.filter(product__id__in=product_ids)  # Get sizes for the corresponding products
	    return sizes


	def get_prods_sizes(self):
	    # Return a dictionary of product sizes where available
	    sizes = {}
	    for key, value in self.trolley.items():
	        if isinstance(value, dict) and 'size' in value:
	            sizes[key] = value['size']
	        else:
	            sizes[key] = None  # Handle cases where there's no size (e.g., when value is an int)
	    return sizes



	def get_quants(self):
	    # Create a dictionary to store quantities by product ID and size
	    quantities = {}
	    for key, value in self.trolley.items():
	        if isinstance(value, dict) and 'quantity' in value:
	            product_id = key.split('_')[0]  # Get the product ID from the key
	            quantities[product_id] = value['quantity']  # Store the quantity by product ID
	    return quantities



	def update(self, product, quantity, size=None):
	    # Use the product's ID to store the product in the trolley
	    product_id = str(product)  # Ensure product is represented as a string
	    product_qty = int(quantity)  # Convert quantity to int directly
	    product_size = str(size) if size else None  # Convert size to string if it exists

	    # Create a unique key for the trolley item based on product ID and size
	    key = product_id
	    if product_size:
	        key = f"{product_id}_{product_size}"

	    # Debugging: Print the trolley before updating
	    print("Current Trolley:", self.trolley)  # Check current state of the trolley

	    # Logic
	    if key in self.trolley:
	        # If the product with the same size already exists, replace the quantity
	        self.trolley[key]['quantity'] = product_qty
	        print(f"Updated {key} to quantity {self.trolley[key]['quantity']}")  # Debugging statement
	    else:
	        # If the product does not exist, check if the product ID exists
	        existing_key = product_id  # Key without size
	        if existing_key in self.trolley:
	            # If the product ID exists but with a different size, add the new size and quantity
	            self.trolley[key] = {
	                'quantity': product_qty,
	                'size': product_size,
	            }
	            print(f"Added new item {key} with quantity {product_qty}")  # Debugging statement
	        else:
	            # If it's a completely new product with new size
	            self.trolley[key] = {
	                'quantity': product_qty,
	                'size': product_size,
	            }
	            print(f"Added new product {key} with quantity {product_qty}")  # Debugging statement
	    
	    self.session.modified = True  # Mark the session as modified
	    return self.trolley  # Return the updated trolley


	def delete(self, product):
	    product_id = str(product)  # Convert product ID to string

	    # Look for the exact product ID (or size combination) in the keys of the trolley
	    matching_keys = [key for key in self.trolley.keys() if key.startswith(product_id)]

	    # If found, delete it from the trolley
	    if matching_keys:
	        for key in matching_keys:
	            del self.trolley[key]  # Remove the specific product from the trolley
	        self.session.modified = True  # Mark the session as modified


	def get_product_ids(self):
	    # Extract product IDs from the keys
	    return [key.split('_')[0] for key in self.trolley.keys()]

	def get_product_sizes(self):
	    # Extract product IDs from the keys
	    return [key.split('_')[1] for key in self.trolley.keys()]

	def current_trolley(self):

		return self.trolley