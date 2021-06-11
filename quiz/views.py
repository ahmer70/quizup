from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin
from quizapp.models import UserQuizData, userColloction
from .models import Quiz, Question, Choice
from django.views.generic import View
from .forms import CreateQuizForm, CreateQuestionForm
from django.http import JsonResponse

from django.db.models import Sum,Count
# Create your views here.
class CustomerNumJsonView(View):
    def get(self, *args, **kwargs):
        customer_count = UserQuizData.objects.filter(correct=True).count()

        return JsonResponse({'customer_count': customer_count})
# index page of all quizzes


def index(request):
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
    
   

    return render(request, 'quiz/index.html', context)


# specific quiz splash screen
def single_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    num_questions = len(quiz.question_set.all())
    #attemt=userColloction.objects.all()
    # member = userColloction(attempts=request.POST['attemptst'])
    # member.save()
    # deletes quiz and returns to home if no questions created
    if num_questions == 0:
        quiz.delete()
        all_quiz_list = Quiz.objects.all()
        context = {
            'all_quiz_list': all_quiz_list,
        }
        return render(request, 'quiz/index.html', context)

    quiz.num_questions = num_questions
    quiz.save()

    # resets accuracy info to 0
    request.session["num_correct"] = 0
    request.session["num_wrong"] = 0
    
    UserQuizData.objects.filter(user_id=request.user.id,q_category=quiz).delete()
    
                
    context = {
        'quiz': quiz,
        'num_questions': num_questions,
    }

    return render(request, 'quiz/single_quiz.html', context)

import random
# specific question view
def single_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    # forcount=list(Question.objects.filter(quiz=quiz_id))
    # random.shuffle(forcount)
    # suf=[]
    
    # for cc in forcount:
    #     if cc not in suf:
    #         suf.append(cc.question_num) 
    # for ss in suf:
    current_question = quiz.question_set.get(question_num=question_id)
    if request.user.is_authenticated:
        correct = UserQuizData.objects.filter(correct=True, user_id=request.user).count()
        wrong = UserQuizData.objects.filter(wrong=True, user_id=request.user).count()
        all_question = UserQuizData.objects.all()
        points=userColloction.objects.all()
    # Checks if currently on last  oquestionf quiz
    next_or_submit = "Next"
    last_question_check = False
    if question_id == (len(quiz.question_set.all())):
        last_question_check = True
        next_or_submit = "Submit"

    next_question_id = question_id+1

    all_choices = current_question.choice_set.all()
    if request.user.is_authenticated:
        context = {
            'current_question': current_question,
            'all_choices': all_choices,
            'quiz': quiz,
            'next_question_id': next_question_id,
            'last_question_check': last_question_check,
            'next_or_submit': next_or_submit,
            'all_question':all_question,
            'correct': correct,
            'wrong': wrong,
            'points':points,
            
        }
    else:
        context = {
            'current_question': current_question,
            'all_choices': all_choices,
            'quiz': quiz,
            'next_question_id': next_question_id,
            'last_question_check': last_question_check,
            'next_or_submit': next_or_submit,
            
        }
    return render(request, 'quiz/single_question.html', context)


# view that receives info from user's answer to question and determines correctness
def vote(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(question_num=question_id)
    title=Quiz.objects.all()
    
    # all_question = UserQuizData.objects.all()
    # all_question.delete()
    # all_questio = userColloction.objects.all()
    # all_questio.delete()
    # if title.quiz_title.id==current_question.id:
    #     quiz_title=title.id
    correct_answer = current_question.choice_set.get(correct=True)
    # checks if current question is last one
    next_or_submit = "Next"
    if question_id == (len(quiz.question_set.all())):
        next_or_submit = "Submit"

    try:
        selected_choice = current_question.choice_set.get(
            pk=request.POST['choice'])
            
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'quiz/single_question.html', {
            'quiz': quiz,
            'current_question': current_question,
            'error_message': "You didn't select a choice.",
            'next_or_submit': next_or_submit,
            'correct_answer':correct_answer,
            'title':title
            
        
        })
    else:

        # get which choice is the correct answer
        correct_answer = current_question.choice_set.get(correct=True)

        if selected_choice == correct_answer:
            if request.user.is_authenticated:
                new_task = UserQuizData(user_id=request.user, question_id=current_question, correct=True, wrong=False,q_category=quiz)
                new_task.save()
                        
                adda = userColloction(user_p=request.user, user_points=+20,count=+1)
                adda.save()
                
                # if adda.user_points >= 20:
                #     levelu = userColloction(user_p=request.user, level=1)
                #     levelu.save()
                #     print("You are right")

            request.session["num_correct"] += 1
        else:
            if request.user.is_authenticated:
                new_task = UserQuizData(
                    user_id=request.user, question_id=current_question, correct=False, wrong=True,q_category=quiz)
                new_task.save()

            print("You are wrong")
            request.session["num_wrong"] += 1
            
            #menus_presentation.append(correct_answer)
            #return render(request, 'quiz/single_question.html', {'menus_presentation':menus_presentation})
            
        # checks if next page should be results or next question
        if question_id == (len(quiz.question_set.all())):
            return HttpResponseRedirect(reverse('quiz:results' ,args=(quiz.id,)))
            
        else:
            return HttpResponseRedirect(reverse('quiz:single_question', args=(quiz.id, question_id+1,)))


# quiz results page
def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    num_correct = request.session["num_correct"]
    num_wrong = request.session["num_wrong"]
    
    total_questions = num_correct+num_wrong

    # formats accuracy as % with no decimal digits
    accuracy = num_correct/(total_questions)

    accuracy_over_75 = False
    if accuracy >= .75:
        accuracy_over_75 = True

    accuracy_formatted = "{:.0%}".format(accuracy)
    if request.user.is_authenticated:
        
        correct = UserQuizData.objects.filter(correct=True, user_id=request.user,q_category=quiz).count()
        wrong = UserQuizData.objects.filter(wrong=True, user_id=request.user,q_category=quiz).count()
        all_question = UserQuizData.objects.all()
        points=userColloction.objects.all()
        context = {
            'num_correct': num_correct,
            'num_wrong': num_wrong,
            'accuracy_over_75': accuracy_over_75,
            'accuracy_formatted': accuracy_formatted,
            'total_questions': total_questions,
            'quiz': quiz,
            
            'all_question':all_question,
            'correct': correct,
            'wrong': wrong,
            'points':points
        }
    else:
         context = {
        'num_correct': num_correct,
        'num_wrong': num_wrong,
        'accuracy_over_75': accuracy_over_75,
        'accuracy_formatted': accuracy_formatted,
        'total_questions': total_questions,
        'quiz': quiz,
        
    }
    return render(request, 'quiz/results.html', context)


