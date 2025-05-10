// game.js

document.addEventListener('DOMContentLoaded', function () {
  const problemEl     = document.getElementById('problem');
  const poopGrid      = document.getElementById('poop-grid');
  const answerInput   = document.getElementById('answer-input');
  const answerDisplay = document.getElementById('answer-display');
  const resultMessage = document.getElementById('result-message');
  const nextBtn       = document.getElementById('next-btn');
  const correctSound  = document.getElementById('correct-sound');
  const wrongSound    = document.getElementById('wrong-sound');

  // ① 問題をタップするとうんこグリッドを表示
  if (problemEl) {
    problemEl.addEventListener('click', function () {
      poopGrid.classList.remove('hidden');
    });
  }

  // ② 数字ボタンの処理
  document.querySelectorAll('.num-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const v = btn.textContent;
      if (/[0-9]/.test(v)) {
        // 数字入力
        answerInput.value += v;
        answerDisplay.textContent += v;
        // 入力ごとにぷるぷる
        poopGrid.classList.add('jiggle');
        setTimeout(() => poopGrid.classList.remove('jiggle'), 300);
      }
      else if (v === 'C') {
        // クリア
        answerInput.value = '';
        answerDisplay.textContent = '';
      }
    });
  });

  // ③ OK（送信）ボタンの処理
  const submitBtn = document.getElementById('submit-btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', () => {
      if (answerInput.value === '') return;

      // 問題から正解を計算
      const parts = problemEl.textContent.split('×').map(n => n.trim());
      const a = parseInt(parts[0], 10);
      const b = parseInt(parts[1], 10);
      const correct = a * b;
      const userAns = parseInt(answerInput.value, 10);
      const isCorrect = (userAns === correct);

      // サウンドとアニメーション（iPhone対応）
      if (isCorrect) {
        poopGrid.classList.add('correct');
        resultMessage.textContent = '正解！';
        resultMessage.className = 'result-message correct';
        if (correctSound) {
          correctSound.currentTime = 0;
          correctSound.play();
        }
      } else {
        poopGrid.classList.add('wrong');
        resultMessage.textContent = '残念…';
        resultMessage.className = 'result-message wrong';
        if (wrongSound) {
          wrongSound.currentTime = 0;
          wrongSound.play();
        }
      }
      resultMessage.style.display = 'block';

      // 入力エリアを隠す（存在チェック）
      const pad = document.querySelector('.num-pad');
      if (pad) {
        pad.style.display = 'none';
      }
      // 次へボタンを表示（存在チェック）
      if (nextBtn) {
        nextBtn.style.display = 'inline-block';
      }

      // サーバーに回答を POST してポイント更新
      fetch(window.location.href, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({ 'answer': answerInput.value })
      });
    });
  }
});
