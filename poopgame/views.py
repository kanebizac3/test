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