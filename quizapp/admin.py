from django.contrib import admin
from .models import Product,UserQuizData,userColloction
# Register your models here.
admin.site.register(Product)

admin.site.register(UserQuizData)
admin.site.register(userColloction)

