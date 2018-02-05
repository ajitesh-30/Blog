from django import forms
from .models import Topic

class NewTopicForm(forms.ModelForm):
	#Here we are defining the content of models i.e what type of elements it will contiann
	message = forms.CharField(
		widget=forms.Textarea( attrs={'rows': 5, 'placeholder': 'What is on your mind?'}),
		max_length=300,
		help_text='The max length of the text is 255.'
	)
	#This meta class is for the forms
	class Meta:
		model = Topic
		fields = ['subject','message']