document.addEventListener('DOMContentLoaded', () => {
  const answerInput = document.getElementById('hissan-answer');
  const submitBtn = document.getElementById('submit-hissan');
  const result = document.getElementById('hissan-result');

  submitBtn.addEventListener('click', () => {
    const correct = parseInt(answerInput.dataset.correct);
    const userAns = parseInt(answerInput.value);
    if (userAns === correct) {
      result.textContent = 'かいケツ！すばらしい！';
      result.style.color = 'green';
    } else {
      result.textContent = `ぶっぶー！せいかいは ${correct} だよ！`;
      result.style.color = 'red';
    }
  });
});
