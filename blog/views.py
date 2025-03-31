from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comments
from .forms import PostForm, CommentsForm
from django.shortcuts import redirect

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
            comments.author = request.user
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
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})