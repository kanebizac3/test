from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comments, GasolineOwada, PoiSute
from .forms import PostForm, CommentsForm, GasolineOwadaForm, PoiSuteForm
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse  # ここを追加
from django.views.decorators.csrf import csrf_exempt
import json

def post_list(request):
    posts = Post.objects.order_by('-updated_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comments.objects.filter(title=post.title).order_by('created_date')
    liked_comments = request.session.get('liked_comments', [])
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
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'liked_comments': liked_comments})

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

        liked_comments = request.session.get('liked_comments', [])

        if comment.id not in liked_comments:
            # いいね処理
            # 例: comment.good += 1; comment.save()
            liked_comments.append(comment.id)
            request.session['liked_comments'] = liked_comments
            request.session.modified = True  # セッションが変更されたことを明示的に通知
            print(f"コメント {comment.id} にいいね！")
        else:
            print(f"コメント {comment.id} は既にいいね済みです。")

        anchor = str(comment.id)
        # ...    
        return redirect(reverse('post_detail', kwargs={"pk" : post.pk})+f'#comment-{anchor}')
    else:
        return HttpResponse('いいね！は POST リクエストのみ受け付けます', status=405)
    

from .models import Category
from django.db.models import Q

def search_post(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    posts = Post.objects.all().order_by('-updated_date')
    categories = Category.objects.all()

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(text__icontains=query))
    
    if category_id:
        posts = posts.filter(category_id=category_id)

    context = {
        'posts': posts,
        'categories': categories,
        'query': query,
        'selected_category': int(category_id) if category_id else None
    }
    return render(request, 'blog/post_search.html', context)

def map_view(request):
    poi_sute_data = PoiSute.objects.all()
    latitude = request.session.get('current_latitude')
    longitude = request.session.get('current_longitude')
    print("test", latitude)

    if request.method == "POST":
        form = PoiSuteForm(request.POST, request.FILES)
        if form.is_valid():
            poisute = form.save(commit=False)
            if 'image' in request.FILES:
                image = Image.open(request.FILES['image'])
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.thumbnail((300, 300))
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')
                poisute.image = InMemoryUploadedFile(buffer, None, 'thumb.jpg', 'image/jpeg',
                                                    buffer.getbuffer().nbytes, None)
            poisute.latitude = form.cleaned_data.get('latitude') or latitude
            poisute.longitude = form.cleaned_data.get('longitude') or longitude
            poisute.save()
        context = {'poi_sute_data': poi_sute_data, "form": form}
        return render(request, 'blog/poisutemap.html', context)
    else:
        form = PoiSuteForm(initial={
            'latitude': latitude,
            'longitude': longitude})
    context = {'poi_sute_data': poi_sute_data, "form": form}
    return render(request, 'blog/poisutemap.html', context)

from django.conf import settings

def get_poi_sute_data(request):
    poi_sute_data = PoiSute.objects.all().values('latitude', 'longitude', 'description', 'reported_at', 'image')
    data_list = []
    for item in poi_sute_data:
        image_url = None
        if item['image']:
            image_url = settings.MEDIA_URL + str(item['image'])
            print(image_url)
        data_list.append({
            'latitude': item['latitude'],
            'longitude': item['longitude'],
            'description': item['description'],
            'reported_at': item['reported_at'],
            'image_url': image_url,  # 画像の URL を追加
        })
    return JsonResponse(data_list, safe=False)

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # 取得した緯度経度をデータベースに保存するなどの処理
                        # リダイレクト先のURLを生成
            map_url = reverse('map_view')

            print(f"Latitude: {latitude}, Longitude: {longitude}")
            return JsonResponse({'status': 'success', 'message': 'Location saved successfully.', 'redirect_url': map_url})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
