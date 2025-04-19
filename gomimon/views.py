from django.shortcuts import render, redirect, get_object_or_404
from .forms import MapForm
from .models import Map, UserProfile, Egg, UserGomimon
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.contrib import messages
import random

def test(request):
    return render(request, 'gomimon/test.html',)

def map(request):
    form = MapForm()
    map = Map.objects.all().values('latitude', 'longitude', 'description', 'reported_at', 'image', 'category')
    context = {"form": form, "map_data":map}
    return render(request, 'gomimon/map.html', context)

@csrf_exempt
def submit_map_data(request):
    if request.method == "POST":
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
                        map_obj.save()
                    except UserProfile.DoesNotExist:
                        # UserProfile が存在しない場合のエラーハンドリング (通常はありえないはず)
                        print(f"Error: UserProfile not found for user {request.user.username}")

                    if random.random() < 0.5: # 10%の確率で敵と遭遇
                        if UserGomimon.objects.filter(user=request.user).exists():
                            print("test")
                            return JsonResponse({'status': 'success', 'message': '投稿が完了しました。', 'redirect_url': reverse('start_battle')})
                        else:
                            return JsonResponse({'status': 'success', 'message': '投稿が完了しました。', 'redirect_url': reverse('map')})

                    else:

                        return JsonResponse({'status': 'success', 'message': '投稿が完了しました。', 'redirect_url': reverse('map')})
                else:
                    map_obj.save()
                    # ユーザーが認証されていない場合の処理
                    return JsonResponse({'status': 'success', 'message': '投稿が完了しました。', 'redirect_url': reverse('map')})
            else:
                return JsonResponse({'status': 'error', 'message': '位置情報が取得できませんでした。'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'フォームが無効です。', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'POSTリクエストのみ受け付けます。'}, status=405)

def get_map_data(request):
    map_data = Map.objects.all().values('latitude', 'longitude', 'description', 'reported_at', 'image', 'category')
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
            'category': item['category'],
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
    if request.user.is_authenticated:
        items = Map.objects.filter(author=request.user).order_by('-reported_at')
        total = Map.objects.count()
        three_items = items.all()[:3]
        print(three_items)

        return render(request, 'registration/user_profile.html', {"items":three_items, "total":total,})
    else:
        return render(request, 'gomimon/error.html')


def gomimon(request):
    user_gomimon = None
    has_egg = False
    if request.user.is_authenticated:
        try:
            user_gomimon = UserGomimon.objects.get(user=request.user)
            hp_percentage = user_gomimon.gomimon_hp/user_gomimon.gomimon_maxhp*100
        except UserGomimon.DoesNotExist:
            user_gomimon = None
            hp_percentage = None
        
        try:
            Egg.objects.get(user=request.user)
            has_egg = True
        except Egg.DoesNotExist:
            has_egg = False
        

        context = {
            'user_gomimon': user_gomimon,
            'has_egg': has_egg,
            'hp_percentage':hp_percentage,
        }
        return render(request, 'gomimon/gomimon.html', context)
    else:
        return render(request, 'gomimon/error.html')

@login_required

def buy_egg(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        has_egg = Egg.objects.filter(user=request.user).exists()  # ユーザーが卵を持っているか確認

        if has_egg:
            messages.warning(request, "あなたは既に卵を持っています。")
        elif profile.points >= 10:
            profile.points -= 10
            profile.save()
            # 新しい卵を作成してユーザーに紐付ける
            egg = Egg.objects.create(user=request.user)
            egg.save()
            # ここで卵の種類や初期ステータスなどを設定することもできます
            # 例: egg.name = "ノーマルな卵"; egg.save()
            return redirect('user_profile')  # 購入後にポイントログページへリダイレクト
        else:
            print("ポイントが足りません")
            # ポイントが足りない場合の処理 (例: エラーメッセージを表示)
            pass  # TODO: ポイント不足のエラーメッセージ処理
    return redirect('user_profile')  # POSTリクエスト以外の場合はポイントログページへリダイレクト


# ------------戦闘

from django.shortcuts import render
from django.http import JsonResponse
from .game_logic import Monster, Battle, level_up_gomimon, get_level_from_experience_exponential

def start_battle_view(request):
    battle_gomimon = UserGomimon.objects.get(user=request.user)
    kansey = Monster(battle_gomimon.gomimon_name, battle_gomimon.gomimon_hp, battle_gomimon.gomimon_maxhp, battle_gomimon.gomimon_atack, battle_gomimon.gomimon_defence)
    print(battle_gomimon.gomimon_name, battle_gomimon.gomimon_hp, battle_gomimon.gomimon_atack, battle_gomimon.gomimon_defence, battle_gomimon.gomimon_maxhp)
    putirin = Monster("じゃあくなこころ", 10, 10, 5, 1 )
    request.session['battle_state'] = {
        'monster1_hp': kansey.hp,
        'monster2_hp': putirin.hp,
        'monster1_ak': kansey.attack,
        'monster2_ak': putirin.attack,
        'monster1_df': kansey.defense,
        'monster2_df': putirin.defense,                
        'log': [],
        'turn': 0,
        'monster1_name': kansey.name,
        'monster2_name': putirin.name,
        'monster1_max_hp': kansey.maxhp,
        'monster2_max_hp': putirin.maxhp,
        'attack': 1,
        'attacker':0,
        'monster1_img': battle_gomimon.gomimon_image,
        'monster2_img': "jaaku.jpg"
    }
    return render(request, 'gomimon/battle_log.html',{
        'battle_state': request.session['battle_state']
    })

def next_turn_view(request):
    battle_state = request.session.get('battle_state')
    if not battle_state or not (battle_state['monster1_hp'] > 0 and battle_state['monster2_hp'] > 0):
        return JsonResponse({'game_over': True, 'winner': battle_state.get('winner')})

    monster1 = Monster(battle_state['monster1_name'], battle_state['monster1_hp'], battle_state['monster1_max_hp'], battle_state['monster1_ak'], battle_state['monster1_df'])
    monster2 = Monster(battle_state['monster2_name'], battle_state['monster2_hp'], battle_state['monster2_max_hp'], battle_state['monster2_ak'], battle_state['monster2_df'])
    battle = Battle(monster1, monster2)
    battle.turn = battle_state['turn']
    battle.log = battle_state['log']
    
    if battle_state["attack"] % 2 != 0:
        attacker, defender = (monster1, monster2) if random.random() < 0.5 else (monster2, monster1)
        if attacker is monster1:
            battle_state["attacker"] = 0
        else:
            battle_state["attacker"] = 1
        turn_log = battle.simulate_turnA(attacker, defender)
    else:
        if battle_state["attacker"] == 0:
            turn_log = battle.simulate_turnB(monster1, monster2)
        else:
            turn_log = battle.simulate_turnB(monster2, monster1)
        
    battle_state["attack"] += 1
    battle_state['log'].extend(turn_log)
    battle_state['monster1_hp'] = battle.monster1.hp
    battle_state['monster2_hp'] = battle.monster2.hp
    battle_state['turn'] = battle.turn
    request.session['battle_state'] = battle_state

    game_over = not (battle.monster1.is_alive() and battle.monster2.is_alive())
    winner = None
    if game_over:
        winner = battle.monster1.name if not battle.monster2.is_alive() else battle.monster2.name
        user_gomimon = UserGomimon.objects.get(user=request.user)
        user_gomimon.gomimon_hp = battle.monster1.hp
        user_gomimon.save()
        

    battle_state['winner'] = winner
    request.session['battle_state'] = battle_state

    if winner is battle.monster1.name:

        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.add_points(1)
        user_gomimon = UserGomimon.objects.get(user=request.user)
        user_gomimon.gomimon_hp = battle.monster1.hp
        user_gomimon.gomimon_exp += 1
        user_gomimon.save()
        turn_log.append(str(user_profile.user)+"は１ポイントを獲得しました。")
        turn_log.append(str(user_gomimon.gomimon_name)+"は経験値を１ポイントを獲得しました。")
        if get_level_from_experience_exponential(user_gomimon.gomimon_exp, base_exp=10)>user_gomimon.gomimon_level:
            user_gomimon = level_up_gomimon(user_gomimon)
            turn_log.append(str(user_gomimon.gomimon_name)+"は"+str(user_gomimon.gomimon_level)+
                            "にレベルアップしました。")
        user_gomimon.save()

    return JsonResponse({
    'log': turn_log,
    'game_over': game_over,
    'winner': winner,
    'hp_monster1': battle.monster1.hp,
    'hp_monster2': battle.monster2.hp,
    
    })




def hatch_gomimon(request):
    user = request.user  # 現在のユーザーを取得

    if not user.is_authenticated:
        return redirect('login')  # ログインしていない場合はログインページへリダイレクト

    has_gomimon = UserGomimon.objects.filter(user=user).exists()

    if has_gomimon:
        return render(request, 'gomimon/hatch_gomimon.html', {'has_gomimon': True})
    else:
        # ここで新しいゴミモンをユーザーに追加する処理を行う
        # 例：ランダムなゴミモンを生成
        possible_gomimons = [
            ["001_can.png", "カーン"],
            ["002_pack.png", "パックン"],
            ["003_suigara.png", "スイガラン"],
            ["004_bottle.png", "ボートル"],
            ["005_bin.png", "ビーン"]
            ] # 例としてのゴミモン画像ファイル名
        choice = random.choice(possible_gomimons)
        hatched_image = choice[0]
        hatched_name = choice[1] # 例としての名前

        new_gomimon = UserGomimon(user=user, gomimon_name=hatched_name, gomimon_image=hatched_image)
        new_gomimon.gomimon_atack=random.randint(3,5)
        new_gomimon.gomimon_defence=random.randint(1, 3)
        new_gomimon.gomimon_level=1
        new_gomimon.gomimon_maxhp=random.randint(20, 30)
        new_gomimon.gomimon_exp=5
        new_gomimon.gomimon_hp=new_gomimon.gomimon_maxhp

        new_gomimon.save()
        hatched_image_url = f"img/{hatched_image}" 

        try:
            egg = Egg.objects.get(user=user)
            egg.delete()
            has_egg = False # 削除したのでFalseにする
        except:
            pass
        
        return render(request, 'gomimon/hatch_gomimon.html', {
            'has_gomimon': False,
            'hatched_name': hatched_name,
            'hatched_image_url': hatched_image_url,
        })
    
@login_required
def release_gomimon(request):
    if request.method == 'POST':
        user_gomimon = UserGomimon.objects.filter(user=request.user).first()
        if user_gomimon:
            user_gomimon.delete()
    return redirect('gomimon')  # ゴミモン画面へ戻る

from .models import Gomimon
@login_required
def create_gomimon(request):
    if request.method == 'POST':
        # バリデーションと保存
        gomimon = Gomimon(
            name=request.POST['name'],
            image=request.FILES.get('image'),
            gomimon_type=request.POST['type'],
            hp=int(request.POST['hp']),
            attack=int(request.POST['attack']),
            defense=int(request.POST['defense']),
            skill=request.POST['skill'],
            skill_effect=request.POST['skill_effect'],
        )
        gomimon.save()
        return redirect('gomimon')
    return render(request, 'gomimon/create_gomimon.html')

