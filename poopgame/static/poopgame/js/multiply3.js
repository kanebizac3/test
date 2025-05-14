// static/poopgame/js/game.js

document.addEventListener('DOMContentLoaded', function () {
  const problemEl     = document.getElementById('problem');
  const poopGrid      = document.getElementById('poop-grid');
  const answerInput   = document.getElementById('answer-input');
  const answerDisplay = document.getElementById('answer-display');
  const resultMessage = document.getElementById('result-message');
  const nextBtn       = document.getElementById('next-btn');
  const correctSound  = document.getElementById('correct-sound');
  const wrongSound    = document.getElementById('wrong-sound');

  // ① 問題をタップするとグリッドを表示
  if (problemEl) {
    problemEl.addEventListener('click', () => {
      poopGrid.classList.remove('hidden');
    });
  }

  // ② 数字ボタンの処理
  document.querySelectorAll('.num-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const v = btn.textContent;
      if (/[0-9]/.test(v)) {
        answerInput.value += v;
        answerDisplay.textContent = answerInput.value;
        poopGrid.classList.add('jiggle');
        setTimeout(() => poopGrid.classList.remove('jiggle'), 300);
      } else if (v === 'けす') {
        answerInput.value = '';
        answerDisplay.textContent = '';
      }
    });
  });

  // ③ 「解ケツ！」ボタンの処理
  const submitBtn = document.getElementById('submit-btn');
  if (submitBtn) {
    submitBtn.addEventListener('click', () => {
      if (!answerInput.value) return;

      // 正解判定
      const parts   = problemEl.textContent.split('×').map(n => n.trim());
      const a       = parseInt(parts[0], 10);
      const b       = parseInt(parts[1], 10);
      const correct = a * b;
      const userAns = parseInt(answerInput.value, 10);
      const isCorrect = (userAns === correct);

      // アニメーション & メッセージ & サウンド
      if (isCorrect) {
        poopGrid.classList.add('correct');
        resultMessage.textContent = 'かいケツ！';
        resultMessage.className = 'result-message correct';
        if (correctSound) {
          correctSound.currentTime = 0;
          correctSound.play();
        }
      } else {
        poopGrid.classList.add('wrong');
        resultMessage.textContent = 'ブッブー…';
        resultMessage.className = 'result-message wrong';
        if (wrongSound) {
          wrongSound.currentTime = 0;
          wrongSound.play();
        }
      }
      resultMessage.style.display = 'block';

      // 入力部を隠し、次へボタンを表示
      const pad = document.querySelector('.num-pad');
      if (pad) pad.style.display = 'none';
      if (nextBtn) nextBtn.style.display = 'inline-block';

      // サーバーに POST → 302リダイレクトを検知
      fetch(window.location.href, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({ 'answer': answerInput.value })
      })
      .then(response => {
        if (response.redirected) {
          const redirectUrl = response.url;
          // 3秒待ってから遷移
          setTimeout(() => {
            window.location.href = redirectUrl;
          }, 3000);
        }
      })
      .catch(err => console.error('通信エラー', err));
    });
  }
});
