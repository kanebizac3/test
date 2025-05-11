// capitalism.js

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('floating-poops');
    const num = 20;  // 一度に浮かせる数
    
    for (let i = 0; i < num; i++) {
      const elem = document.createElement('div');
      elem.classList.add('floating');
      // ランダムな横位置
      elem.style.left = Math.random() * 100 + 'vw';
      // ランダムなサイズと速度
      const scale = 0.5 + Math.random() * 0.5;
      elem.style.transform = `scale(${scale})`;
      const duration = 6 + Math.random() * 4;
      elem.style.animationDuration = duration + 's';
      elem.style.animationDelay = Math.random() * duration + 's';
      container.appendChild(elem);
    }
  });
  