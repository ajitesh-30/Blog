from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Board
from django.contrib.auth.models import User
from .models import Board,Topic,Post
from .forms import NewTopicForm

def home(request):
	boards = Board.objects.all()
	return render(request,'index.html',{'boards':boards})

def board_topics(request,pk):
	try:
		board = Board.objects.get(pk=pk)
	except Board.DoesNotExist:
		raise Http404
	return render(request,'topics.html',{'board':board})

def new_topic(request,pk):
	board = get_object_or_404(Board,pk=pk)
	user = User.objects.first()
	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save()
			return redirect('board_topics',pk=board.pk)
	else:
		form = NewTopicForm()
	return render(request,'new_topic.html',{'board':board,'form':form})
# Create your views here.
