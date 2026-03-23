from django.shortcuts import render

from blog.models import Category, Post


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