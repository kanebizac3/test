function addDigit(n) {
    document.getElementById("answer").value += n;
  }
  
  function clearAnswer() {
    document.getElementById("answer").value = "";
  }

  function showNextButton() {
    document.getElementById("next-question-area").style.display = "block";
  }

  function goToNextQuestion() {
    location.reload();
  }

  function triggerBigExplosion() {
    const poops = document.querySelectorAll(".poop");
    const vw = window.innerWidth;
    const vh = window.innerHeight;
  
    poops.forEach((p, idx) => {
      // ランダムに飛ぶ方向・距離を設定
      const dx = (Math.random() - 0.5) * vw * 1.2;  // ±60%画面幅
      const dy = (Math.random() - 0.5) * vh * 1.2;  // ±60%画面高
      p.style.setProperty("--dx", `${dx}px`);
      p.style.setProperty("--dy", `${dy}px`);
  
      // 少しずつずらしてアニメ開始
      setTimeout(() => {
        p.classList.add("explode-large");
      }, idx * 50);  // 50msズラしで波状に爆発
    });
  
    // アニメ後に次へ
    showNextButton();
  }
  
  // ★ 先頭で要素を取得
const explosionSound = document.getElementById('explosion-sound');
const wrongMessage    = document.getElementById('wrong-message');
const wrongBoy        = document.getElementById('wrong-boy');
const fartImg         = document.getElementById('fart-img');
  
  function submitAnswer() {
    const answer = parseInt(document.getElementById("answer").value, 10);
    const poops = document.querySelectorAll(".poop");
    const correctArea = document.getElementById("correct-area");
  
    if (answer === correctAnswer) {
      // ① 正解メッセージを出す
      correctArea.style.display = "block";
  
      // ② うんこを便器へ吸い込むアニメーション
      poops.forEach((p, idx) => {
        setTimeout(() => {
          p.style.transform = "translateY(200px) scale(0.1)";
          p.style.opacity   = "0";
        }, idx * 100);
      });
  
      // ③ アニメーション後、自動で次の問題（ページリロード）
    //   const delay = poops.length * 100 + 1200;
    //   setTimeout(() => {
    //     location.reload();
    //   }, delay);
    showNextButton();
  
    } else {
        // ① 爆発音を再生
    explosionSound.currentTime = 0;
    explosionSound.play();

    // ② 「ぶっぶー」文字・少年画像・オナラ画像を表示
    wrongMessage.style.display = "block";
    wrongBoy.style.display     = "block";
    fartImg.style.display      = "block";
      // 不正解：爆発アニメーション後リロード
    triggerBigExplosion();

    }
  }
  

  