# Django Blog Project

A comprehensive Django blog application demonstrating MVT (Model-View-Template) architecture with both function-based and class-based views.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [MVT Architecture](#mvt-architecture)
  - [Model](#model)
  - [View](#view)
  - [Template](#template)
- [Creating Views](#creating-views)
  - [Function-Based Views](#function-based-views)
  - [Class-Based Views](#class-based-views)
- [URL Configuration](#url-configuration)
- [Template Usage](#template-usage)
- [Category List View Example](#category-list-view-example)

## Setup Instructions

Follow these steps to set up the Django blog project locally:

### 1. Clone Repository

```bash
git clone <repository-url>
cd Simpleblog2026s1
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- Django==6.0.3
- pillow==12.1.1 (for image handling)
- psycopg2-binary==2.9.11 (PostgreSQL adapter)
- python-dotenv==1.2.2 (environment variables)

### 4. Setup Local Database

Edit `Simpleblog2026s1/settings.py` to configure your database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
Simpleblog2026s1/
├── manage.py
├── requirements.txt
├── Simpleblog2026s1/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
└── templates/
    ├── base.html
    └── blog/
        ├── index.html
        ├── post_list.html
        ├── post_detail.html
        └── ...
```

## MVT Architecture

Django follows the Model-View-Template (MVT) pattern:

### Model

Models define the structure of your data. Located in `blog/models.py`:

```python
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    header_image = models.ImageField(upload_to='images/', blank=True, null=True)
    title_tag = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    snippet = models.CharField(max_length=100)
    likes = models.ManyToManyField(User, related_name='likes')
    
    def __str__(self):
        return self.category.name + ' - ' + self.title
```

### View

Views handle the logic and process user requests. Located in `blog/views.py`:

#### Example: index() Function-Based View

```python
def index(request):
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'categories': categories})
```

This view:
1. Receives the HTTP request
2. Queries all categories from the database
3. Renders the `blog/index.html` template with categories data

### Template

Templates define the HTML structure and display data. Located in `templates/blog/`:

#### Example: index.html Template

```html
{% extends 'base.html' %}

{% block title %}Blog Home{% endblock %}

{% block content %}
<div class="container">
    <h1>Blog Categories</h1>
    <div class="row">
        {% for category in categories %}
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ category.name }}</h5>
                        <a href="{% url 'category_detail' category.id %}" 
                           class="btn btn-primary">View Posts</a>
                    </div>
                </div>
            </div>
        {% empty %}
            <p>No categories found.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### URL Configuration

Connect views to URLs in `blog/urls.py`:

```python
from django.urls import path
from blog.views import index, category_detail, post_detail

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]
```

Include app URLs in main `Simpleblog2026s1/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

## Creating Views

### Function-Based Views

Simple and explicit, great for custom logic:

```python
def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'blog/category.html', {'category': category})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post.html', {'post': post})

def create_category(request):
    if request.method == 'POST':
        name = request.POST['category_name']
        category = Category.objects.create(name=name)
        return redirect('category_detail', category_id=category.id)
    return render(request, 'blog/create_category.html')
```

### Class-Based Views

Provide reusable patterns and built-in functionality:

```python
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  # Default: object_list

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'   # Default: object
```

## URL Configuration

### Function-Based View URLs

```python
urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create_category/', create_category, name='create_category'),
]
```

### Class-Based View URLs

```python
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post_detail/<int:pk>/detail/', PostDetailView.as_view(), name='post_detail_view'),
]
```

Note: Class-based views use `.as_view()` method and `<int:pk>` for primary key.

## Template Usage

### Using URL Names in Templates

Use the `{% url %}` template tag to create links:

```html
<!-- In base.html navigation -->
<nav>
    <a href="{% url 'index' %}">Home</a>
    <a href="{% url 'create_category' %}">Create Category</a>
    <a href="{% url 'post_list' %}">Posts</a>
</nav>

<!-- Linking to specific objects -->
<a href="{% url 'category_detail' category.id %}">{{ category.name }}</a>
<a href="{% url 'post_detail' post.id %}">{{ post.title }}</a>
```

### Template Inheritance

Extend base template:

```html
{% extends 'base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <div class="container">
        <h1>Page Content</h1>
        <!-- Your content here -->
    </div>
{% endblock %}
```

### Accessing Model Data

```html
<!-- Displaying category data -->
<h2>{{ category.name }}</h2>

<!-- Displaying post data -->
<h3>{{ post.title }}</h3>
<p>By {{ post.author.username }} on {{ post.post_date|date:"F d, Y" }}</p>
<p>{{ post.body }}</p>

<!-- Looping through related objects -->
{% for post in category.post_set.all %}
    <h4>{{ post.title }}</h4>
    <p>{{ post.snippet }}</p>
{% endfor %}
```

## Category List View Example

Here's a complete example of creating a category list view:

### 1. Add View Function

In `blog/views.py`:

```python
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})
```

### 2. Create Template

Create `templates/blog/category_list.html`:

```html
{% extends 'base.html' %}

{% block title %}All Categories{% endblock %}

{% block content %}
<div class="container">
    <h1>All Categories</h1>
    
    {% if categories %}
        <div class="row">
            {% for category in categories %}
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{{ category.name }}</h5>
                            <p class="card-text">
                                {{ category.post_set.count }} post(s) in this category
                            </p>
                            <a href="{% url 'category_detail' category.id %}" 
                               class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>No categories found.</p>
        <a href="{% url 'create_category' %}" class="btn btn-success">
            Create First Category
        </a>
    {% endif %}
</div>
{% endblock %}
```

### 3. Add URL Pattern

In `blog/urls.py`:

```python
from blog.views import category_list

urlpatterns = [
    # ... existing patterns ...
    path('categories/', category_list, name='category_list'),
]
```

### 4. Add Navigation Link

In `templates/base.html`:

```html
<li class="nav-item">
    <a class="nav-link" href="{% url 'category_list' %}">All Categories</a>
</li>
```

## Best Practices

1. **Use URL names** instead of hardcoding URLs
2. **Follow Django conventions** for template organization
3. **Use function-based views** for simple, custom logic
4. **Use class-based views** for standard CRUD operations
5. **Keep business logic** in views, not templates
6. **Use template inheritance** to avoid code duplication
7. **Validate user input** in forms and views
8. **Use proper error handling** with try-catch blocks

## Running the Project

After setup, you can access different pages:

- Home: `http://127.0.0.1:8000/`
- Posts List: `http://127.0.0.1:8000/posts/`
- Create Category: `http://127.0.0.1:8000/create_category/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

