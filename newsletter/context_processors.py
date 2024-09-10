from .forms import SubscriptionForm
from .models import Article

def subscription_form(request):
	return {
		'subscription_form': SubscriptionForm()
	}

def articles_processor(request):
    return {
        'articles': Article.objects.all()
    }