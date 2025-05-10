// subtract3.js

document.addEventListener('DOMContentLoaded', () => {
    const problemEl     = document.getElementById('problem');
    const poopGrid      = document.getElementById('poop-grid');
    const toiletGrid    = document.getElementById('toilet-grid');
    const answerInput   = document.getElementById('answer-input');
    const answerDisplay = document.getElementById('answer-display');
    const resultMessage = document.getElementById('result-message');
    const form          = document.getElementById('answer-form');
    const correctSound  = document.getElementById('correct-sound');
    const wrongSound    = document.getElementById('wrong-sound');
  
    // 問題タップで表示
    problemEl.addEventListener('click', () => {
      poopGrid.classList.remove('hidden');
      toiletGrid.classList.remove('hidden');
    });
  
    // 数字パッド
    document.querySelectorAll('.num-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const v = btn.textContent;
        if (/[0-9]/.test(v)) {
          answerInput.value += v;
          answerDisplay.textContent += v;
          document.querySelectorAll('.poop-img').forEach(p => {
            p.classList.add('jiggle');
            setTimeout(() => p.classList.remove('jiggle'), 300);
          });
        } else if (v === 'けす') {
          answerInput.value = '';
          answerDisplay.textContent = '';
        }
      });
    });
  
    // OKボタン
    document.getElementById('submit-btn').addEventListener('click', () => {
      if (!answerInput.value) return;
  
      // 問題から a, b を取得
      const [aStr, bStr] = problemEl.textContent.split('−').map(s => s.trim());
      const a = parseInt(aStr, 10), b = parseInt(bStr, 10);
      const correct = a - b;
      const userAns = parseInt(answerInput.value, 10);
      const isCorrect = (userAns === correct);
  
      // うんこ要素配列
      const poops = Array.from(document.querySelectorAll('.poop-img'));
  
      // 再生後にフォーム送信する関数
      const finishAndSubmit = (audio) => {
        const holdAfter = 500;  // 再生終了後ホールド(ms)
        audio.addEventListener('ended', () => {
          setTimeout(() => form.submit(), holdAfter);
        }, { once: true });
        // 再生開始
        audio.currentTime = 0;
        audio.play();
      };
  
      // 結果表示＆アニメーション
      if (isCorrect) {
        poops.slice(0, b).forEach((p, i) => {
          setTimeout(() => p.classList.add('toilet-away'), i * 200);
        });
        resultMessage.textContent = `かいケツ🍑！ のこりは ${correct} です💩`;
        resultMessage.className = 'result-message correct';
        resultMessage.style.display = 'block';
  
        // 効果音→終了後 submit
        if (correctSound) finishAndSubmit(correctSound);
      } else {
        const vw = window.innerWidth, vh = window.innerHeight;
        poops.forEach((p, i) => {
          const dx = (Math.random()-0.5)*vw;
          const dy = (Math.random()-0.5)*vh;
          p.style.setProperty('--dx', `${dx}px`);
          p.style.setProperty('--dy', `${dy}px`);
          setTimeout(() => p.classList.add('explode'), i * 100);
        });
        resultMessage.textContent = `ブッブー… せいかいは ${correct} です`;
        resultMessage.className = 'result-message wrong';
        resultMessage.style.display = 'block';
  
        // 効果音→終了後 submit
        if (wrongSound) finishAndSubmit(wrongSound);
      }
  
      // 入力部を隠す
      document.querySelector('.num-pad').style.display = 'none';
    });
  });
  