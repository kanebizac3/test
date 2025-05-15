let commands = [];
let currentX = 0;
let currentY = 0;

function renderGrid(stage) {
  const gridEl = document.getElementById("grid");
  gridEl.innerHTML = "";
  stage.forEach((row, y) => {
    row.forEach((cell, x) => {
      const div = document.createElement("div");
      div.className = `cell ${cell}`;
      div.dataset.x = x;
      div.dataset.y = y;
      div.textContent = (cell === "poop") ? "💩" : (cell === "goal") ? "🚽" : "";
      gridEl.appendChild(div);
    });
  });
}

function addCommand(dir) {
  commands.push(dir);
  document.getElementById("message").textContent = "命令：" + commands.join(" → ");
}

function runProgram() {
  currentX = 0;
  currentY = 0;
  let i = 0;

  function step() {
    if (i >= commands.length) return;
    let cmd = commands[i++];
    let [dx, dy] = [0, 0];
    if (cmd === "up") dy = -1;
    if (cmd === "down") dy = 1;
    if (cmd === "left") dx = -1;
    if (cmd === "right") dx = 1;

    const newX = currentX + dx;
    const newY = currentY + dy;

    if (
      newY >= 0 && newY < stageData.length &&
      newX >= 0 && newX < stageData[0].length &&
      stageData[newY][newX] !== "obstacle"
    ) {
      currentX = newX;
      currentY = newY;
    } else {
      document.getElementById("message").textContent = "ぶっぶー！進めないよ";
      return;
    }

    updatePoopPosition();
    if (stageData[currentY][currentX] === "goal") {
      document.getElementById("message").textContent = "かいケツ！🚽";
      return;
    }

    setTimeout(step, 500);
  }

  step();
}

function updatePoopPosition() {
  document.querySelectorAll(".cell").forEach(cell => {
    cell.textContent = "";
  });
  const newCell = document.querySelector(`.cell[data-x="${currentX}"][data-y="${currentY}"]`);
  if (newCell) newCell.textContent = "💩";
}

function resetGame() {
  commands = [];
  currentX = 0;
  currentY = 0;
  renderGrid(stageData);
  document.getElementById("message").textContent = "";
}
document.addEventListener("DOMContentLoaded", () => {
  renderGrid(stageData);
});
