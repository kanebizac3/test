// 数字ボタン入力
function addDigit(ch) {
    const input = document.getElementById('answer');
    input.value += ch;
  }
  function clearAnswer() {
    document.getElementById('answer').value = '';
  }
  
  function submitAnswer() {
    const answer = parseInt(document.getElementById('answer').value, 10);
    const container = document.getElementById('poop-container');
    const poops = container.querySelectorAll('.poop');
  
    if (answer === correctAnswer) {
      // 正解：戻す分だけ「removed」クラスを付与
      for (let i = 0; i < subtract; i++) {
        const idx = poops.length - 1 - i;
        if (poops[idx]) {
          poops[idx].classList.add('removed');
        }
      }
    } else {
      // 不正解：fart エフェクトで10個のうんこを噴き出す
      for (let i = 0; i < 10; i++) {
        const newPoop = document.createElement('span');
        newPoop.classList.add('poop', 'fart');
        newPoop.textContent = '💩';
        // ランダムな水平位置
        const x = Math.random() * container.clientWidth;
        newPoop.style.left = `${x}px`;
        newPoop.style.bottom = `0px`;
        container.appendChild(newPoop);
      }
    }
  }
  