from django.views import View
from .models import Post, Category, Tag, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

# Blog listing view
def blog(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    categories = Category.objects.all() 

    # Pagination
    paginator = Paginator(posts, 6)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'posts': paginated_posts,
        'categories': categories
    }

    return render(request, 'blog.html', context)

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)

    # Pagination
    paginator = Paginator(posts, 5)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'posts': paginated_posts,
        'category': category,
        'categories': Category.objects.all(),
        'current_category': category,
    }
    return render(request, 'category.html', context)

def tags(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)

    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'posts': paginated_posts,
        'tags': Tag.objects.all(),
        'current_tag': tag
    }
    return render(request, 'tags.html', context)

# Single post detail view
class BlogSingle(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        related_posts = post.get_related_posts()
        session_key = f'viewed_post_{post.id}'
        if not request.session.get(session_key, False):
            post.views_count += 1
            post.save(update_fields=['views_count'])
            request.session[session_key] = True
        
        context = {
            'post': post, 
            'related_posts': related_posts,
        }

        return render(request, 'blog-single.html', context)