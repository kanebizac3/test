from django.shortcuts import render

def programing(request):
    return render(request, 'poopgame/programing.html')

from django.shortcuts import render
import random

def poopsub(request):
    # 問題設定
    original = random.randint(5, 9)           # 元のうんこ個数
    subtract = random.randint(1, original-1)  # 戻すうんこ個数
    correct = original - subtract

    # テンプレート用に「0 から original-1 まで」のリストを作成
    poop_indices = list(range(original))

    return render(request, 'poopgame/poopsub.html', {
        'original': original,
        'subtract': subtract,
        'correct': correct,
        'poop_indices': poop_indices,
    })

# poopgame/views.py

from django.shortcuts import render, redirect
from .models import UnpPoint
import random

def multiply(request):
    # GET: 新しい問題を表示
    rows = random.randint(2, 5)
    cols = random.randint(2, 5)
    total = rows * cols
    return render(request, 'poopgame/multiply.html', {
        'rows': rows,
        'cols': cols,
        'rows_range': range(rows),
        'cols_range': range(cols),
        # フラグ類は未チェックの状態
        'checked': False,
    })

def multiply_check(request):
    if request.method != 'POST':
        return redirect('multiply')

    # POSTデータ取得
    rows = int(request.POST['rows'])
    cols = int(request.POST['cols'])
    correct = rows * cols
    try:
        user_answer = int(request.POST.get('answer', '').strip())
    except ValueError:
        user_answer = None

    result = (user_answer == correct)

    print("DEBUG multiply_check:", user_answer, correct, result)

    # 正解なら1うんPを加算
    if result and request.user.is_authenticated:
        unp, _ = UnpPoint.objects.get_or_create(user=request.user)
        unp.add_point(1)

    return render(request, 'poopgame/multiply.html', {
        'rows': rows,
        'cols': cols,
        'rows_range': range(rows),
        'cols_range': range(cols),
        'checked': True,
        'result': result,
        'correct_answer': correct,
        'user_answer': user_answer,
    })


def poopadd(request):
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    total = num1 + num2

    # ここでリスト化して渡す
    context = {
        'num1': num1,
        'num2': num2,
        'total': total,
        'num1_list': list(range(num1)),
        'num2_list': list(range(num2)),
        'checked': False,
    }
    return render(request, 'poopgame/poopadd.html', context)

from .models import UnpPoint
def poopadd_check(request):
    if request.method == 'POST':
        num1 = int(request.POST['num1'])
        num2 = int(request.POST['num2'])
        total = num1 + num2
        user_answer_raw = request.POST.get('answer', '').strip()
        try:
            user_answer = int(user_answer_raw)
            result = (user_answer == total)
        except ValueError:
            user_answer = None
            result = False

        # 正解したら1うんP加算
        if result and request.user.is_authenticated:
            unp, created = UnpPoint.objects.get_or_create(user=request.user)
            unp.add_point(1)

        context = {
            'num1': num1,
            'num2': num2,
            'total': total,
            'num1_list': list(range(num1)),
            'num2_list': list(range(num2)),
            'checked': True,
            'user_answer': user_answer,
            'result': result,
        }
        return render(request, 'poopgame/poopadd.html', context)
    # GET で来た場合はリダイレクト
    return redirect('poopadd')

# ーーーー掛け算２
# poopgame/views.py

from django.shortcuts import render
import random

def poopmultiply2(request):
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    total = num1 * num2
    return render(request, 'poopgame/poopmultiply2.html', {
        'num1': num1,
        'num2': num2,
        'total': total,
        'num1_list': range(num1),
        'num2_list': range(num2),
    })

def poopmultiply2_check(request):
    num1 = int(request.POST['num1'])
    num2 = int(request.POST['num2'])
    correct_answer = int(request.POST['correct_answer'])
    user_answer = request.POST.get('answer', '')

    checked = True
    try:
        result = int(user_answer) == correct_answer
    except:
        result = False

    return render(request, 'poopgame/poopmultiply2.html', {
        'num1': num1,
        'num2': num2,
        'total': correct_answer,
        'num1_list': range(num1),
        'num2_list': range(num2),
        'checked': checked,
        'result': result,
    })


# ーーーーー割り算
from django.shortcuts import render
import random

def divide(request):
    if request.method == 'POST':
        # POSTデータ取得
        groups = int(request.POST.get('groups', 0))           # 分けるグループ数
        per_group = int(request.POST.get('per_group', 0))     # 1グループあたりの数（正解）
        total = int(request.POST.get('total', 0))             # 合計
        correct_answer = per_group
        user_answer_str = request.POST.get('answer', '').strip()
        try:
            user_answer = int(user_answer_str)
        except (ValueError, TypeError):
            user_answer = None

        result = (user_answer == correct_answer)

                # 正解したら1うんP加算
        if result and request.user.is_authenticated:
            unp, created = UnpPoint.objects.get_or_create(user=request.user)
            unp.add_point(1)

        context = {
            'groups': groups,
            'per_group': per_group,
            'total': total,
            'rows_range': list(range(per_group)),   # 行数 = 1グループあたりの数
            'cols_range': list(range(groups)),      # 列数 = グループ数
            'correct_answer': correct_answer,
            'checked': True,
            'result': result,
            'user_answer': user_answer,
        }
        return render(request, 'poopgame/divide.html', context)

    # GET時：新しい問題を生成（必ず余りなく分けられる数に）
    groups    = random.randint(2, 5)
    per_group = random.randint(2, 5)
    total     = groups * per_group

    context = {
        'groups': groups,
        'per_group': per_group,
        'total': total,
        'rows_range': list(range(per_group)),
        'cols_range': list(range(groups)),
        'correct_answer': per_group,
        'checked': False,
    }
    return render(request, 'poopgame/divide.html', context)

def home(request):
    # 仮にセッションに保存されている場合（なければ0）
    unp_points = request.session.get('unp_points', 0)
    return render(request, 'poopgame/home.html', {'unp_points': unp_points})

# ユーザー登録
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def poopgame_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # うんこアプリのホームへ
    else:
        form = UserCreationForm()
    return render(request, 'poopgame/register.html', {'form': form})

from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

