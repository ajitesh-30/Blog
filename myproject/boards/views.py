from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.views.generic import UpdateView
from django.utils import timezone
from .models import Board,Topic,Post
from .forms import NewTopicForm,PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def home(request):
	boards = Board.objects.all()
	return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
	board = get_object_or_404(Board,pk=pk)
	topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
	page = request.GET.get('page', 1)
	paginator = Paginator(topics, 2)
	try:
		topics = paginator.page(page)
	except PageNotAnInteger:
		topics = paginator.page(1)
	except EmptyPage:
		topics = paginator.page(paginator.num_pages)
	return render(request, 'topics.html', {'board': board, 'topics': topics})

def topic_posts(request,pk,topic_pk):
	topic = get_object_or_404(Topic,pk=topic_pk)
	topic.views += 1
	topic.save()
	return render(request,'topic_posts.html',{'topic':topic})

@login_required
def new_topic(request,pk):
	board = get_object_or_404(Board,pk=pk)
	user = User.objects.first()
	form = NewTopicForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = request.user
			topic.save()
			post = Post.objects.create(
				message=message,
				topic=topic,
				created_by=request.user
			)
			return redirect('board_topics',pk=board.pk,topic_pk=topic.pk)
		else:
			form = NewTopicForm()
	return render(request,'new_topic.html',{'board':board,'form':form})

@login_required
def reply_topic(request,pk,topic_pk):
	form = PostForm(request.POST or None)
	topic = get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
	if request.method == 'POST':
		if form.is_valid():
			post  = form.save(commit=False)
			post.topic = topic
			post.created_by = request.user
			post.save()
			return redirect('topic_posts',pk=pk,topic_pk=topic_pk)
		else:
			form = PostForm()
	return render(request,'reply_topic.html',{'topic':topic,'form':form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
	model = Post
	fields = ('message',)
	template_name = 'edit_post.html'
	pk_url_kwarg = 'post_pk'
	context_object_name = 'post'

	def form_valid(self,form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts',pk=post.topic.board.pk,topic_pk=post.topic.pk)
