
document.addEventListener('DOMContentLoaded', () => {
  const answerInput = document.getElementById('answer');
  const numButtons = document.querySelectorAll('.num-pad button');

  // 数字・C・← ボタンのクリック処理
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
  if (form) {
    form.addEventListener('submit', e => {
      if (!answerInput.value) {
        e.preventDefault();
        alert('まず数字を入力してください！');
      }
    });
  }

  // -------------------------------
  // 回答後のアニメーションと効果音
  // -------------------------------
  const poops = document.querySelectorAll('.poop');
  const explodeSound = document.getElementById('explode-sound');
  const flushSound = document.getElementById('flush-sound');

  if (isChecked) {
    if (isCorrect) {
      // 正解 → うんこを流すアニメ
      if (flushSound) {
        flushSound.currentTime = 0;
        flushSound.play();
      }
      poops.forEach((p, i) => {
        setTimeout(() => {
          p.classList.add('flow');
        }, i * 100);
      });
    } else {
      // 間違い → 爆発＆飛び散るアニメ
      if (explodeSound) {
        explodeSound.currentTime = 0;
        explodeSound.play();
      }

      const vw = window.innerWidth;
      const vh = window.innerHeight;
      poops.forEach((p, i) => {
        const dx = (Math.random() - 0.5) * vw * 1.5;
        const dy = (Math.random() - 0.5) * vh * 1.5;
        p.style.setProperty('--dx', `${dx}px`);
        p.style.setProperty('--dy', `${dy}px`);
        setTimeout(() => {
          p.classList.add('explode-fly');
        }, i * 100);
      });
    }
  }
});
  