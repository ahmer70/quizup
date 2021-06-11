from django.urls import path

# importing views from views..py
from .views import GeeksCreate, create_questionview
from .views import GeeksList, UserQuizList
from .views import GeeksDetailView
from .views import GeeksUpdateView,option
from .views import GeeksDeleteView
from .views import viewQuestion,openQuestion,update_view,delete_view,QuestionList
from .views import create_quiz, create_question,AddMore
# app_name = 'dashboard'
urlpatterns = [

    #path('createview/', create_questionview.as_view(), name="createview"),
    path('', GeeksList.as_view(template_name="user_list.html"), name="user_profile"),
	path('viewQuestion/', viewQuestion, name='viewQuestion'),
	path('create/', create_quiz, name='create_quiz'),
	path('create/<int:quiz_id>/<int:question_id>/', create_question, name='create_question'),
	path('openQuestion/<int:id>', openQuestion, name='openQuestion'),
    path('<id>/question_update', update_view ,name="question_update"),
    path('<id>/delete_question', delete_view ,name='delete_question'),
    path('<id>/questionList_update', QuestionList ,name="questionList_update"),
    path('<id>/add_more', AddMore ,name="add_more"),
    path('add', GeeksCreate.as_view(template_name="user_form.html")),

    path('<pk>/', GeeksDetailView.as_view(template_name="user_detail.html"),
         name="user_detail"),
    path('<pk>/update/', GeeksUpdateView.as_view(template_name="user_update.html"),
         name="user_update"),
    path('<pk>/delete/', GeeksDeleteView.as_view(template_name="user_confirm_delete.html")),

    path('UserQuizList', UserQuizList.as_view(), name="UserQuizList"),
    
    path('<pk>/option/', option.as_view(), name="option_s"),

    #  path('create/', create_quiz, name='create_quiz'),

    # # ex: /quiz/create/7/2/
    # path('create/<int:quiz_id>/<int:question_id>/', create_question, name='create_question'),


]
