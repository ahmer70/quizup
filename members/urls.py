from django.urls import path
from .views import PasswordsChangeView
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import GeeksCreate
from .views import GeeksList
from .views import GeeksDetailView
from .views import GeeksUpdateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'members'
urlpatterns = [
    #path('register',UserRegistrationView.as_view() ,name='register'),
    path('register',views.register ,name='register'),
    path('login/', views.login_view, name ='login'),
    path('password/',PasswordsChangeView.as_view(template_name='registration/edit_password.html') ),
    path('success', views.success, name='success'),
   	  path('userdata', GeeksList.as_view(template_name = "base.html"),name="userdata"),
	path('add', GeeksCreate.as_view() ),
	
	path('profile/<int:pk>/', GeeksDetailView.as_view(template_name = "geeksmodel_detail.html"),name="profile"),
	 path('update/<pk>/', GeeksUpdateView.as_view(template_name = "geeksmodel_update.html"),name="update"),


    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)