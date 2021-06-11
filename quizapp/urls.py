
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import questionView
from quiz.views import index
urlpatterns = [
   path('', index,name='homepage'),
  # path('about', views.about,name='about'),
  path('about', views.about,name='about'),
    #path('about', questionView.as_view(),name='about'),
   path('contact', views.contact,name='contact'),
  # path('login', views.login,name='login'),
   path('home/', views.index,name='home')
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)