document.addEventListener('DOMContentLoaded', () => {
  const answerInput = document.getElementById('hissan-answer');
  const submitBtn = document.getElementById('submit-hissan');
  const result = document.getElementById('hissan-result');

  // グローバルで使えるように window に追加
  window.addDigit = function(digit) {
    answerInput.value += digit;
  };

  window.clearAnswer = function() {
    answerInput.value = '';
  };

  submitBtn.addEventListener('click', () => {
    // correct_answer を数値に変換
    const correct = Number(answerInput.dataset.correct); // 数値に変換
    const userAns = parseInt(answerInput.value, 10); // 入力された答えを数値として取得

    // デバッグ：正解を確認
    console.log("correct_answer:", correct);
    console.log("user_answer:", userAns);

    // ユーザーの答えが有効な数値であり、正解と一致するかをチェック
    if (!isNaN(userAns)) {
      if (userAns === correct) {
        result.textContent = 'かいケツ！すばらしい！';
        result.style.color = 'green';
      } else {
        result.textContent = `ぶっぶー！せいかいは ${correct} だよ！`;
        result.style.color = 'red';
      }
    } else {
      result.textContent = '無効な入力です。もう一度試してください。';
      result.style.color = 'orange';
    }
  });
});
