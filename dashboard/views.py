from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse
from members.models import User
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin
from quizapp.models import UserQuizData, userColloction
from quiz.models import Quiz, Question, Choice
from django.views.generic import View
from quiz.forms import CreateQuizForm, CreateQuestionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class GeeksCreate(CreateView):

	# specify the model for create view
	model = User

	# specify the fields to be displayed

	fields = ['first_name', 'last_name']

	success_url ="/"



@method_decorator(login_required, name='dispatch')
class GeeksList(ListView):
	# specify the model for list view
	model = User

 
class GeeksDetailView(DetailView):
	# specify the model to use
    model = User
    template_name='user_detail.html'
    def get_context_data(self,*args,**kwargs):
        context=super(GeeksDetailView, self).get_context_data(*args,**kwargs)
        total_points=userColloction.objects.filter(user_p=self.kwargs['pk'] ).aggregate(Sum('user_points')).get('user_points__sum', 0.00) 
        context["total_points"]=total_points
        return context
        

class GeeksUpdateView(UpdateView):
    # specify the model you want to use
    model = User
    # specify the fields
    # fields = '__all__'
    fields = [
        "first_name",
        "last_name"
    ]
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"


class GeeksDeleteView(DeleteView):
    # specify the model you want to use
    model = User
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/"


#USerQuiz

class UserQuizList(ListView):
	# specify the model for list view
    model = UserQuizData
    template_name='User_Quiz_Data/UserQuiz_list.html'
    def get_context_data(self,*args,**kwargs):
        user=User.objects.all()
        quiz=Quiz.objects.all()
        context=super(UserQuizList, self).get_context_data(*args,**kwargs)
        total_correct=UserQuizData.objects.filter(correct=True).count()
        total_wrong=UserQuizData.objects.filter(wrong=True).count()
        points=UserQuizData.objects.all()
        context["total_correct"]=total_correct
        context["total_wrong"]=total_wrong
        context["points"]=points
        context["user"]=user
        context["quiz"]=quiz
        return context

  
class UserQuizDetailView(DetailView):
	# specify the model to use
	model = UserQuizData


class UserQuizUpdateView(UpdateView):
    # specify the model you want to use
    model = UserQuizData
    # specify the fields
    # fields = '__all__'
    fields = [
        "first_name",
        "last_name"
    ]
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"


class UserQuizDeleteView(DeleteView):
    # specify the model you want to use
    model = UserQuizData
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/"
    

class create_questionview(CreateView):
    model:Question
    form_class:CreateQuestionForm
    template_name:'question.html'
# view for create quiz page
@login_required
def create_quiz(request):
    if not request.user.is_superuser:
        return HttpResponse('The user is not superuser')
    # If this is a POST request then process the Form data
    else:
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = CreateQuizForm(request.POST)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                quiz_name = form.cleaned_data['quiz_name']
                num_questions = form.cleaned_data['num_questions']

                new_quiz = Quiz(quiz_title=quiz_name, num_questions=num_questions)
                new_quiz.save()

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('create_question', args=(new_quiz.id, 1,)))

        # If this is a GET (or any other method) create the default form.
        else:
            form = CreateQuizForm()

        context = {
            'form': form,
        }

        return render(request, 'create_questions/create_quiz.html', context)


# view for create quiz page

def create_question(request, quiz_id, question_id):

    # gets current quiz
    quiz = Quiz.objects.get(pk=quiz_id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateQuestionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            question_text = form.cleaned_data['question_text']

            choice1 = form.cleaned_data["choice1_text"]
            choice1_correctness = form.cleaned_data["choice1_correctness"]

            choice2 = form.cleaned_data["choice2_text"]
            choice2_correctness = form.cleaned_data["choice2_correctness"]

            choice3 = form.cleaned_data["choice3_text"]
            choice3_correctness = form.cleaned_data["choice3_correctness"]

            choice4 = form.cleaned_data["choice4_text"]
            choice4_correctness = form.cleaned_data["choice4_correctness"]

            # creates question in quiz
            question = Question(
                quiz=quiz, question_text=question_text, question_num=question_id)
            question.save()

            # creates choices for questions
            question.choice_set.create(
                choice_text=choice1, correct=choice1_correctness)
            question.choice_set.create(
                choice_text=choice2, correct=choice2_correctness)
            question.choice_set.create(
                choice_text=choice3, correct=choice3_correctness)
            question.choice_set.create(
                choice_text=choice4, correct=choice4_correctness)

            # redirect to home if done or next create question page if not
            if question_id == quiz.num_questions:
                return HttpResponseRedirect(reverse('viewQuestion'))
            else:
                return HttpResponseRedirect(reverse('create_question', args=(quiz_id, question_id+1,)))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CreateQuestionForm()

    if question_id == quiz.num_questions:
        next_submit = "Submit"
    else:
        next_submit = "Next"

    context = {
        'form': form,
        'question_num': question_id,
        'next_submit': next_submit,

    }

    return render(request, 'create_questions/create_question.html', context)

from django.db.models import Sum,Count
def viewQuestion(request):
    all_quiz_list = Quiz.objects.all()
   
  
    if request.user.is_authenticated:
        # duplicates = UserQuizData.objects.values('question_id').annotate(name_count=Count('question_id')).filter(name_count__gt=1)
        # records = UserQuizData.objects.filter(user_id=request.user,question_id__in=[item['question_id'] for item in duplicates])
        # show_presentation_list = []
        # menus_presentation = []
         # menus_presentation.append(menu)
        # for menu in records:
        #     if menu.question_id and menu.question_id in duplicates:
        #         attemt = userColloction(user_p=request.user, attempts=2)
        #         attemt.save()
        #         # show_presentation_list.append(menu.question_id)
        #         # menus_presentation.append(menu)
        #         print("yes")
        all_question = UserQuizData.objects.all()
        
        show_presentation_list = []
        menus_presentation = []
        for item in all_question:
            
            if request.user.id == item.user_id.id:
                if item.correct: 
                    show_presentation_list.append(item.question_id)
                    correct_answer = Choice.objects.filter(correct=True)
                    #for ite in correct_answer:
                    #if item.correct==correct_answer:
                        #correct_answer=correct_answer
                    
                
        
        total_points = userColloction.objects.filter(user_p=request.user).aggregate(Sum('user_points')).get('user_points__sum', 0.00) 
        context = {
            'all_quiz_list': all_quiz_list,
            
            'total_points':total_points,
            # 'records':records,
            #'correct_answer':correct_answer,
            'all_question':all_question,
            'show_presentation_list':show_presentation_list,
            'menus_presentation':menus_presentation
        }
    else:
         context = {
        
        'all_quiz_list': all_quiz_list,
    }
    # userl=userColloction.objects.filter(user_points__isnull=True).count()
    
   

    return render(request, 'create_questions/viewQuestion.html', context)

def openQuestion(request,id):
    question=Question.objects.filter(quiz=id)
    form=Choice.objects.all()
    content={
        'question':question,
        'form':form
        }
    return render(request, 'create_questions/openQuestion.html',content )
from .forms import  QuestionForm,QuestionListForm
from quiz.models import  Choice
def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Question, id = id)
 
    # pass the object as instance in form
    form = QuestionForm(request.POST or None, instance = obj)
    
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/dashboard/viewQuestion/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "create_questions/update_view.html", context)
from django.shortcuts import (get_object_or_404,
							render,
							HttpResponseRedirect)




# delete view for details
def delete_view(request, id,):
	# dictionary for initial data with
	# field names as keys
	context ={}

	# fetch the object related to passed id
	obj = get_object_or_404(Question, id = id)


	if request.method =="POST":
		# delete object
		obj.delete()
		# after deleting redirect to
		# home page
		return HttpResponseRedirect("/dashboard/viewQuestion/")

	return render(request, "create_questions/delete_view.html", context)

class option(UpdateView):
    model=Question
    template_name="option.html"
    fields=[
        "question_text"
    ]
 
    
    
    success_url ="/"
def QuestionList(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    # fetch the object related to passed id
    obj = get_object_or_404(Quiz, id = id)
 
    # pass the object as instance in form
    form = QuestionListForm(request.POST or None, instance = obj)
    
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/dashboard/viewQuestion/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "create_questions/questionList_update.html", context)

def AddMore(request, id):

    # gets current quiz
    quiz = Quiz.objects.get(pk=id)
    add=Question.objects.filter(quiz=id).count()
    addone=add
    addone=addone+1
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CreateQuestionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            question_text = form.cleaned_data['question_text']
            choice1 = form.cleaned_data["choice1_text"]
            choice1_correctness = form.cleaned_data["choice1_correctness"]

            choice2 = form.cleaned_data["choice2_text"]
            choice2_correctness = form.cleaned_data["choice2_correctness"]

            choice3 = form.cleaned_data["choice3_text"]
            choice3_correctness = form.cleaned_data["choice3_correctness"]

            choice4 = form.cleaned_data["choice4_text"]
            choice4_correctness = form.cleaned_data["choice4_correctness"]

            # creates question in quiz
            question = Question(
                quiz=quiz, question_text=question_text, question_num=addone)
            question.save()

            # creates choices for questions
            question.choice_set.create(
                choice_text=choice1, correct=choice1_correctness)
            question.choice_set.create(
                choice_text=choice2, correct=choice2_correctness)
            question.choice_set.create(
                choice_text=choice3, correct=choice3_correctness)
            question.choice_set.create(
                choice_text=choice4, correct=choice4_correctness)

            # redirect to home if done or next create question page if not
            
            return HttpResponseRedirect("/dashboard/viewQuestion/")

    # If this is a GET (or any other method) create the default form.
    else:
        form = CreateQuestionForm()

    

    context = {
        'form': form,
        'add':add
    }

    return render(request, 'create_questions/add_more.html', context)
