from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CreatePostForm, PostUpdateForm
from blog.models import Category, Post, UserProfile


# Create your views here.
def index(request):
    categories = Category.objects.all()
    return render(request, 'blog/index.html',
                  {'categories': categories})

def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'blog/category.html',
                  {'category': category})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post.html',
                  {'post': post})

def create_category(request):
    if request.method == 'POST':
        name = request.POST['category_name']
        category = Category.objects.create(name=name)
        return redirect('category_detail', category_id=category.id)
    return render(request, 'blog/create_category.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostUpdateForm
    success_url = reverse_lazy('post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        github_url = request.POST['github_url']
        linkedin_url = request.POST['linkedin_url']

        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email)
        user.set_password(password)
        user.save()
        profile = UserProfile(user=user,
                              github_url=github_url,
                              linkedin_url=linkedin_url)
        profile.save()
        return redirect('login')
    return render(request, 'registration/register.html')

