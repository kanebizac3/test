document.addEventListener('DOMContentLoaded', () => {
    const answerInput     = document.getElementById('answer');
    const numButtons      = document.querySelectorAll('.num-pad button');
    const form            = document.getElementById('answer-form');
    const correctSound    = document.getElementById('correct-sound');
    const wrongSound      = document.getElementById('wrong-sound');
    const poops           = document.querySelectorAll('#poop-grid .poop');
    const nextContainer   = document.getElementById('next-btn-container');
  
    // HTML属性から状態を取得
    const body = document.body;
    const checked = body.dataset.checked === 'true';
    const isCorrect = body.dataset.result === 'true';
  
    // 数字パッドの動作
    numButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const v = btn.textContent;
        if (v === 'C')          answerInput.value = '';
        else if (v === '←')     answerInput.value = answerInput.value.slice(0, -1);
        else                    answerInput.value += v;
      });
    });
  
    // 判定後の演出
    if (checked) {
      form.style.display = 'none';
  
      if (isCorrect) {
        correctSound.currentTime = 0;
        correctSound.play();
        poops.forEach((p, i) => setTimeout(() => p.classList.add('flow'), i * 100));
      } else {
        wrongSound.currentTime = 0;
        wrongSound.play();
        const vw = window.innerWidth, vh = window.innerHeight;
        poops.forEach((p, i) => {
          const dx = (Math.random() - 0.5) * vw * 1.2;
          const dy = (Math.random() - 0.5) * vh * 1.2;
          p.style.setProperty('--dx', `${dx}px`);
          p.style.setProperty('--dy', `${dy}px`);
          setTimeout(() => p.classList.add('explode-large'), i * 150);
        });
      }
  
      nextContainer.style.display = 'block';
    }
  });
  