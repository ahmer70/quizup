from django.urls import path

from . import views
#from dashboard .views import create_quiz,create_question
from quiz.views import  CustomerNumJsonView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'quiz'
urlpatterns = [
    # ex: /quiz/
    path('', views.index, name='index'),
    path('json',CustomerNumJsonView.as_view(),name="customers_json"),
    # ex: /quiz/5/
    path('<int:quiz_id>/', views.single_quiz, name='single_quiz'),

    # ex: /quiz/5/3/
    path('<int:quiz_id>/<int:question_id>/', views.single_question, name='single_question'),

    # ex: /quiz/5/3/vote/
    path('<int:quiz_id>/<int:question_id>/vote/', views.vote, name='vote'),

    # ex: /quiz/5/results/
    path('<int:quiz_id>/results/', views.results, name='results'),

    # # ex: /quiz/create/
    # path('create/', create_quiz, name='create_quiz'),

    # # ex: /quiz/create/7/2/
    # path('create/<int:quiz_id>/<int:question_id>/', create_question, name='create_question'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)