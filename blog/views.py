from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comments, GasolineOwada
from .forms import PostForm, CommentsForm, GasolineOwadaForm
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.http import HttpResponse

def post_list(request):
    posts = Post.objects.order_by('-updated_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comments.objects.filter(title=post.title).order_by('created_date')
    if request.method == "POST":
        form = CommentsForm(request.POST, request.FILES)
        if form.is_valid():
            comments = form.save(commit=False)
            if request.user.is_authenticated:
                comments.author = request.user
            else:
                # 認証されていない場合は特定のユーザーを割り当て（例：ユーザー名が"guest"のユーザー）
                comments.author, created = User.objects.get_or_create(username="guest")
            if 'image' in request.FILES:
                image = Image.open(request.FILES['image'])
                if image.mode != 'RGB': #RGBAモードの場合
                   image = image.convert('RGB') #RGBモードへ変更
                image.thumbnail((300, 300))  # 画像を300x300にリサイズ
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')  # JPEG形式で保存
                comments.image = InMemoryUploadedFile(buffer, None, 'thumb.jpg', 'image/jpeg',
                                                    buffer.getbuffer().nbytes, None)

            comments.title = post.title
            # ポストを更新する
            post.updated_date = timezone.now()
            comments.created_date = timezone.now()
            post.save()
            comments.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentsForm()    
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                # 認証されていない場合は特定のユーザーを割り当て（例：ユーザー名が"guest"のユーザー）
                post.author, created = User.objects.get_or_create(username="guest")
            if 'image' in request.FILES:
                image = Image.open(request.FILES['image'])
                if image.mode != 'RGB': #RGBAモードの場合
                   image = image.convert('RGB') #RGBモードへ変更
                image.thumbnail((300, 300))  # 画像を300x300にリサイズ
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')  # JPEG形式で保存
                post.image = InMemoryUploadedFile(buffer, None, 'thumb.jpg', 'image/jpeg',
                                                    buffer.getbuffer().nbytes, None)
            post.updated_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def top(request):
    return render(request, 'blog/top.html', {})


def life(request):
    if request.method == "POST":
        form = GasolineOwadaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            latest = GasolineOwada.objects.latest('created_date')
            render(request, 'blog/life.html', {'form': form, "latest": latest})
    
    else:
        form = GasolineOwadaForm()
        latest = GasolineOwada.objects.latest('created_date')
    return render(request, 'blog/life.html', {'form': form, "latest": latest})


def analytic(request):
    return render(request, 'blog/analytic.html', {})

def policy(request):
    return render(request, 'blog/plibacypolicy.html', {})

def term(request):
    return render(request, 'blog/terms_of_use.html', {})

def mission_promise(request):
    return render(request, 'blog/mission.html', {})

def like_post_view(request, post_id, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comments, id=comment_id)
        post = get_object_or_404(Post, id=post_id)

        if comment.good == None:
            comment.good = 0
        comment.good +=1 
        comment.save()
        # いいね処理
        # 例: ユーザーがいいね済みでないか確認し、いいねを追加/削除する
        # ...    
        return redirect('post_detail', pk=post.id)
    else:
        return HttpResponse('いいね！は POST リクエストのみ受け付けます', status=405)