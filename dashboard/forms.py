from django import forms
from members.models import User


# creating a form
class GeeksForm(forms.ModelForm):
	template_name = "geeksmodel_form.html"
	# create meta class
	class Meta:
		# specify model to be used
		model = User

		# specify fields to be used
		fields = [
			"first_name",
			"last_name",
		]
from django import forms
from quiz.models import Question,Choice,Quiz


# creating a form
class QuestionForm(forms.ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = Question

		# specify fields to be used
		fields = [
			"question_text"]

class QuestionListForm(forms.ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = Quiz

		# specify fields to be used
		fields = [
			"quiz_title","num_questions"]