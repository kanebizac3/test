function splitGroup(groupId, count) {
  const group = document.getElementById(groupId);
  group.innerHTML = '';
  const template = document.getElementById('poop-template');

  for (let i = 0; i < count; i++) {
    const poop = template.content.cloneNode(true);
    group.appendChild(poop);
  }
}

function addDigit(d) {
  const input = document.getElementById('answer');
  input.value += d;
}
function clearAnswer() {
  document.getElementById('answer').value = '';
}
function deleteLast() {
  const input = document.getElementById('answer');
  input.value = input.value.slice(0, -1);
}
