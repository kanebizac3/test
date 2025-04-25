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

def multiply(request):
    # 縦（rows）と横（cols）をランダムに決定
    rows = random.randint(2, 5)
    cols = random.randint(2, 5)
    total = rows * cols

    # テンプレートでイテレートできるようにリスト化
    rows_range = list(range(rows))
    cols_range = list(range(cols))

    return render(request, 'poopgame/multiply.html', {
        'rows': rows,
        'cols': cols,
        'correct_answer': total,
        'rows_range': rows_range,
        'cols_range': cols_range,
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


def poopadd_check(request):
    if request.method == 'POST':
        num1 = int(request.POST['num1'])
        num2 = int(request.POST['num2'])
        total = num1 + num2
        user_answer = int(request.POST['answer'])
        result = (user_answer == total)

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
