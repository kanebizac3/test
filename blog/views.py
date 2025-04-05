from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comments
from .forms import PostForm, CommentsForm
from django.shortcuts import redirect
from django.contrib.auth.models import User

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comments.objects.filter(title=post.title).order_by('created_date')
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            if request.user.is_authenticated:
                comments.author = request.user
            else:
                # 認証されていない場合は特定のユーザーを割り当て（例：ユーザー名が"guest"のユーザー）
                comments.author, created = User.objects.get_or_create(username="guest")
            comments.title = post.title
            comments.created_date = timezone.now()
            comments.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentsForm()    
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                # 認証されていない場合は特定のユーザーを割り当て（例：ユーザー名が"guest"のユーザー）
                post.author, created = User.objects.get_or_create(username="guest")
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def top(request):
    return render(request, 'blog/top.html', {})

def life(request):
    return render(request, 'blog/life.html', {})

def analytic(request):
    return render(request, 'blog/analytic.html', {})

def policy(request):
    return render(request, 'blog/plibacypolicy.html', {})

def term(request):
    return render(request, 'blog/terms_of_use.html', {})

def mission_promise(request):
    return render(request, 'blog/mission.html', {})
