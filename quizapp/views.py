from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,UserQuizData

from django.views.generic import ListView



class  questionView(ListView):
    
    mode=UserQuizData
    template_name='data.html'

def home(request):
	questionda = Product.objects.all()

	return render(request, 'index.html', { 'questionda': questionda})
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact_us.html')

def index(request):
    return render(request,'home.html')
# Create your views here.
