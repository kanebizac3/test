from django.shortcuts import render
from .models import UnpPoint, AttemptLog

def programing(request):
    return render(request, 'poopgame/programing.html')

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
    num1 = random.randint(1, 14)
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

        # ③ ログを保存
        if request.user.is_authenticated:
            AttemptLog.objects.create(
                user           = request.user,
                operation      = 'add',
                operand_a      = num1,
                operand_b      = num2,
                user_answer    = user_answer if user_answer is not None else -1,
                correct_answer = total,
                is_correct     = result
            )

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

from django.shortcuts import render, redirect
import random

def unko_kakezan(request):
    # — セッション初期化 —
    if 'points' not in request.session:
        request.session['points'] = 0

    if request.user.is_authenticated:
        unp, _ = UnpPoint.objects.get_or_create(user=request.user)
        request.session['points'] = unp.point

    if request.method == 'POST':
        # — 回答処理 —
        user_answer = request.POST.get('answer')
        try:
            user_answer = int(user_answer)
        except (TypeError, ValueError):
            user_answer = None

        a = request.session.get('a')
        b = request.session.get('b')
        correct_answer = a * b
        is_correct = (user_answer == correct_answer)

        # ログ保存
        if request.user.is_authenticated:
            AttemptLog.objects.create(
                user           = request.user,
                operation      = 'mul',
                operand_a      = a,
                operand_b      = b,
                user_answer    = user_answer if user_answer is not None else -1,
                correct_answer = correct_answer,
                is_correct     = is_correct
            )

        # モデルにもDBにも正解ポイントを反映
        if is_correct and request.user.is_authenticated:
            unp.add_point(1)
            request.session['points'] = unp.point  # DB値に合わせる

        context = {
            'a': a, 'b': b,
            'a_range': range(a), 'b_range': range(b),
            'answered': True, 'is_correct': is_correct,
            'points': request.session['points'],
            'correct_answer': correct_answer,
        }
    else:
        # — 新しい問題を作成 —
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        request.session['a'] = a
        request.session['b'] = b

        context = {
            'a': a, 'b': b,
            'a_range': range(a), 'b_range': range(b),
            'answered': False,
            'points': request.session['points'],
        }

    return render(request, 'poopgame/multiply3.html', context)

# views.py

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import UnpPointHistory

def weekly_ranking(request):
    now = timezone.now()
    week_ago = now - timedelta(days=1)

    # 過去7日間ポイント合計TOP3
    raw = (
        UnpPointHistory.objects
        .filter(timestamp__gte=week_ago)
        .values('user__username')
        .annotate(total=Sum('points'))
        .order_by('-total')[:3]
    )

    # ビュー側で順位と画像パスを付与
    podium = []
    for idx, entry in enumerate(raw, start=1):
        podium.append({
            'rank': idx,
            'username': entry['user__username'],
            'total': entry['total'],
            # staticファイル上のパス（例: poopgame/img/podium1.png）
            'img_path': f'poopgame/img/podium{idx}.png',
        })

    return render(request, 'poopgame/weekly_ranking.html', {
        'podium': podium,
    })

from django.shortcuts import render
import random

def unko_hikizan(request):
    # セッションポイント初期化
    if 'points' not in request.session:
        request.session['points'] = 0
    if request.user.is_authenticated:
        unp, _ = UnpPoint.objects.get_or_create(user=request.user)
        request.session['points'] = unp.point

    if request.method == 'POST':
        # ユーザー解答取得
        try:
            user_answer = int(request.POST.get('answer',''))
        except:
            user_answer = None

        # セッションから問題を取得
        a = request.session.get('a', 0)
        b = request.session.get('b', 0)
        correct_answer = a - b
        is_correct = (user_answer == correct_answer)

        # ③ ログを保存
        if request.user.is_authenticated:
            AttemptLog.objects.create(
                user           = request.user,
                operation      = 'sub',
                operand_a      = a,
                operand_b      = b,
                user_answer    = user_answer if user_answer is not None else -1,
                correct_answer = correct_answer,
                is_correct     = is_correct
            )

        # 正解ならポイント追加
        if is_correct and request.user.is_authenticated:
            unp.add_point(1)
            request.session['points'] = unp.point

        # 結果表示用コンテキスト
        context = {
            'a': a,
            'b': b,
            'poop_range': range(a),     # うんこ表示用
            'toilet_range': range(b),   # 便器表示用
            'answered': True,
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'points': request.session['points'],
        }
        return render(request, 'poopgame/subtract3.html', context)

    # GET: 新しい問題を生成
    a = random.randint(3, 9)
    b = random.randint(1, a-1)
    request.session['a'] = a
    request.session['b'] = b

    context = {
        'a': a,
        'b': b,
        'poop_range': range(a),
        'toilet_range': range(b),
        'answered': False,
        'points': request.session['points'],
    }
    return render(request, 'poopgame/subtract3.html', context)
