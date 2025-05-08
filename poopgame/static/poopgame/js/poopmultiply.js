// static/poopgame/js/poopmultiply.js
function addDigit(d) {
    const input = document.getElementById("answer");
    input.value += d;
  }
  
  function clearAnswer() {
    document.getElementById("answer").value = "";
  }
  
  function deleteLast() {
    const input = document.getElementById("answer");
    input.value = input.value.slice(0, -1);
  }
  