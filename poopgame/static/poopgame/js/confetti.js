// confetti.js

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('confetti-container');
    const colors = ['#f8c94b','#f78da7','#8bd3c7','#f3a683','#786fa6'];
    const count = 80;
  
    for (let i = 0; i < count; i++) {
      const conf = document.createElement('div');
      conf.classList.add('confetti');
      // ランダムな色
      conf.style.background = colors[Math.floor(Math.random() * colors.length)];
      // ランダムな初期位置とサイズ
      conf.style.left = Math.random() * 100 + '%';
      conf.style.width = conf.style.height = (5 + Math.random() * 8) + 'px';
      // ランダムなアニメーション遅延
      conf.style.animationDelay = (Math.random() * 5) + 's';
      container.appendChild(conf);
    }
  });
  