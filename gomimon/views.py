from django.shortcuts import render, redirect
from .forms import MapForm
from .models import Map, UserProfile
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

def test(request):
    return render(request, 'gomimon/test.html',)

def map(request):
    form = MapForm()
    map = Map.objects.all().values('latitude', 'longitude', 'description', 'reported_at', 'image')
    context = {"form": form, "map_data":map}
    return render(request, 'gomimon/map.html', context)

@csrf_exempt
def submit_map_data(request):
    if request.method == "POST":
        print("1")
        form = MapForm(request.POST, request.FILES)
        if form.is_valid():
            map_obj = form.save(commit=False)
            if 'image' in request.FILES:
                image = Image.open(request.FILES['image'])
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.thumbnail((300, 300))
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')
                map_obj.image = InMemoryUploadedFile(buffer, None, 'thumb.jpg', 'image/jpeg',
                                                    buffer.getbuffer().nbytes, None)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print(latitude)
            if latitude and longitude:
                map_obj.latitude = latitude
                map_obj.longitude = longitude
                if request.user.is_authenticated:
                    map_obj.author = request.user
                            # ポイントを加算
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    user_profile.add_points(1)
                except UserProfile.DoesNotExist:
                    # UserProfile が存在しない場合のエラーハンドリング (通常はありえないはず)
                    print(f"Error: UserProfile not found for user {request.user.username}")
                map_obj.save()
            
                return JsonResponse({'status': 'success', 'message': '投稿が完了しました。', 'redirect_url': reverse('map')})
            else:
                return JsonResponse({'status': 'error', 'message': '位置情報が取得できませんでした。'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'フォームが無効です。', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'POSTリクエストのみ受け付けます。'}, status=405)

def get_map_data(request):
    map_data = Map.objects.all().values('latitude', 'longitude', 'description', 'reported_at', 'image')
    data_list = []
    for item in map_data:
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
            request.session['current_latitude'] = latitude
            request.session['current_longitude'] = longitude
            return JsonResponse({'status': 'success', 'message': '位置情報を保存しました。'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    
# ---ユーザー登録----
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm  # デフォルトのユーザー作成フォームも利用可能
from .forms import UserRegistrationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後、自動的にログインさせる場合
            return redirect('registration_success')  # 登録成功後のリダイレクト先
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/registration_success.html')


from django.contrib.auth.decorators import login_required

@login_required
def some_action(request):
    request.user.profile.add_points(50)  # 50ポイント加算
    return redirect('some_success_url')

def user_profile(request):
    return render(request, 'registration/user_profile.html')

def gomimon(request):
    return render(request, 'gomimon/gomimon.html')
