from django.shortcuts import render
from .models import Posts
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.
def home(request):
	context={
		'posts':Posts.objects.all()
	}
	return render(request,'blog/home.html',context)
def about(request):
	return render(request,'blog/about.html',{'title':'about'})


class PostListView(ListView):
	model=Posts
	template_name='blog/home.html'
	context_object_name='posts'
	ordering=['-date_posted']

class PostDetailView(DetailView):
	model=Posts

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model=Posts
	success_url='/'
	
	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False	

	
class PostCreateView(LoginRequiredMixin,CreateView):
	model=Posts
	fields=['title','content']

	def form_valid(self,form):
		form.instance.author=self.request.user	
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model=Posts
	fields=['title','content']

	def form_valid(self,form):
		form.instance.author=self.request.user	
		return super().form_valid(form)		

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False		