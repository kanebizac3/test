// static/poopgame/js/bonus.js

document.addEventListener('DOMContentLoaded', () => {
    const imgs         = Array.from(document.querySelectorAll('.poop-img'));
    const timerEl      = document.getElementById('time');
    const form         = document.getElementById('bonus-form');
    const selectedIn   = document.getElementById('selected-input');
    const cheer        = document.getElementById('cheer-sound');
    const explodeSnd   = document.getElementById('explode-sound');
    let time            = TIME_LIMIT;
  
    // タイマー開始
    const timerID = setInterval(() => {
      time--;
      timerEl.textContent = time;
      if (time <= 0) {
        clearInterval(timerID);
        submitSelection(-1);
      }
    }, 1000);
  
    // 正解のうんこ画像をウインクに差し替え
    const correctImg = imgs.find(img => +img.dataset.index === CORRECT_INDEX);
    if (correctImg) {
      correctImg.src = WINK_URL;
    }
  
    // 画像クリックで判定
    imgs.forEach(img => {
      img.addEventListener('click', () => {
        if (time <= 0) return;
  
        clearInterval(timerID);
        const idx = +img.dataset.index;
        if (idx === CORRECT_INDEX) {
          // 正解演出
          showBonusOverlay();
          if (cheer) {
            cheer.currentTime = 0;
            cheer.play();
            cheer.addEventListener('ended', () => submitSelection(idx), { once: true });
          } else {
            submitSelection(idx);
          }
        } else {
          // 不正解演出
          const vw = window.innerWidth, vh = window.innerHeight;
          explodeSnd.currentTime = 0;
          explodeSnd.play();
          img.classList.add('shake');
          setTimeout(() => img.classList.add('explode'), 600);
          setTimeout(() => submitSelection(-1), 1400);
        }
      });
    });
  
    function submitSelection(idx) {
      selectedIn.value = idx;
      form.submit();
    }
  
    function showBonusOverlay() {
      const overlay = document.createElement('div');
      overlay.id = 'bonus-popup';
      overlay.textContent = 'うんP +10!';
      document.body.appendChild(overlay);
      requestAnimationFrame(() => overlay.classList.add('show'));
    }
  });
  