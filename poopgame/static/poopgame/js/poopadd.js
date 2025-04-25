// ページ読み込み後にボタン操作を有効化
document.addEventListener('DOMContentLoaded', () => {
    const answerInput = document.getElementById('answer');
    const numButtons  = document.querySelectorAll('.num-pad button');
    
    // 数字・C・← ボタンのクリック
    numButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const v = btn.textContent;
        if (v === 'C') {
          answerInput.value = '';
        } else if (v === '←') {
          answerInput.value = answerInput.value.slice(0, -1);
        } else {
          answerInput.value += v;
        }
      });
    });
    
    // フォーム送信前チェック（空なら警告）
    const form = document.getElementById('answer-form');
    form.addEventListener('submit', e => {
      if (!answerInput.value) {
        e.preventDefault();
        alert('まず数字を入力してください！');
      }
    });
  });
  