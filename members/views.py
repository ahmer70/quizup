from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.urls import  reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.contrib import messages
from django.http import request
from quizapp.models import userColloction
from .forms import  SignupForm
# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse

from .models import User
from django.shortcuts import render
class GeeksCreate(CreateView):
    form_class=SignupForm
    template_name="registration/registration.html"
    success_url=reverse_lazy('login')


     

    def get_object(self):
        return self.request.user

class GeeksList(ListView):

	# specify the model for list view
	model = User



class GeeksDetailView(DetailView):
	# specify the model to use
	model = User
	
	
class GeeksUpdateView(UpdateView):
    # specify the model you want to use
    model = User
  
    # specify the fields
    fields = [
        "first_name",
        "last_name","email","bio","profile_pic","country"
    ]
  
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"
from django.contrib.messages.views import SuccessMessageMixin

from .forms import SignupForm,PasswordChangingForm


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm,UserLoginForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system ####################################
            htmly = get_template('registration/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'ahmerarain18@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/registration.html', {'form': form, 'title':'reqister here'})
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "registration/login.html", context)
class PasswordsChangeView(PasswordChangeView):
    #form_class=PasswordChangeForm
    form_class=PasswordChangingForm
    success_url=reverse_lazy('success')

def success(request):
	return HttpResponse('successfully uploaded')# Python program to view
