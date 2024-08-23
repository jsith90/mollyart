from .trolley import Trolley

# Create context processor so our trolley can work on all pages
def trolley(request):
	# return the default data from our Trolley
	return {'trolley': Trolley(request)}