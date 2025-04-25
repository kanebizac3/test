// グリッド設定
const GRID_SIZE = 5;
const AREA = document.getElementById('game-area');
const CELL = AREA.clientWidth / GRID_SIZE;

// 要素取得
const playerEl = document.getElementById('player');
const poopEl   = document.getElementById('poop');
const toiletEl = document.getElementById('toilet');
const programEl= document.getElementById('program');

// プレイヤーの座標 (px, py) と向き pdir（0=↑,1=→,2=↓,3=←）
let px = 0, py = GRID_SIZE - 1, pdir = 0;
let hasPoop = true;  // 初期状態：手に💩を持っている

// 初期配置描画
function init() {
  updateElement(playerEl, px, py, pdir);
  updateElement(poopEl, px, py, pdir);
}
window.addEventListener('load', init);

// 座標・向きに合わせて要素を配置する
function updateElement(el, x, y, dir=0) {
  el.style.left      = `${x * CELL}px`;
  el.style.top       = `${y * CELL}px`;
  el.style.transform = `rotate(${dir * 90}deg)`;
}

// コマンドボタン登録
document.querySelectorAll('#cmd-list button').forEach(btn => {
  btn.addEventListener('click', () => {
    programEl.value += btn.textContent + '\n';
  });
});

// クリア
document.getElementById('clear').addEventListener('click', () => {
  programEl.value = '';
});

// 実行
document.getElementById('run').addEventListener('click', () => {
  const cmds = programEl.value.trim().split('\n').filter(Boolean);
  runCommands(cmds);
});

// コマンドを順次実行
function runCommands(cmds) {
  let step = 0;
  const interval = setInterval(() => {
    if (step >= cmds.length) { clearInterval(interval); return; }
    execute(cmds[step].trim());
    step++;
  }, 700);
}

// 単一コマンドの解釈
function execute(cmd) {
  switch(cmd) {
    case '前へ':   moveForward(); break;
    case '左向く': turn(-1);     break;
    case '右向く': turn(1);      break;
    case '拾う':   pickup();     break;
    case '入れる': drop();       break;
    case '流す':   flushPoop();  break;
  }
}

// 前進処理
function moveForward() {
  let nx = px, ny = py;
  if      (pdir === 0) ny--;
  else if (pdir === 1) nx++;
  else if (pdir === 2) ny++;
  else if (pdir === 3) nx--;
  if (nx < 0 || nx >= GRID_SIZE || ny < 0 || ny >= GRID_SIZE) return;
  px = nx; py = ny;
  updateElement(playerEl, px, py, pdir);
  if (hasPoop) updateElement(poopEl, px, py, pdir);
}

// 向き変更
function turn(delta) {
  pdir = (pdir + delta + 4) % 4;
  updateElement(playerEl, px, py, pdir);
  if (hasPoop) updateElement(poopEl, px, py, pdir);
}

// 拾う（拡張用：地面から拾う）
function pickup() {
  hasPoop = true;
  updateElement(poopEl, px, py, pdir);
}

// ドロップ
function drop() {
  hasPoop = false;
  poopEl.style.opacity = '0';
}

// 流す（便器前かつ手持ちあり）
function flushPoop() {
  const tx = GRID_SIZE - 1, ty = GRID_SIZE - 1;
  if (hasPoop && px === tx && py === ty) {
    // 吸い込みアニメーション
    const pr = poopEl.getBoundingClientRect();
    const tr = toiletEl.getBoundingClientRect();
    const dx = tr.left + tr.width/2  - (pr.left + pr.width/2);
    const dy = tr.top  + tr.height/4 - (pr.top  + pr.height/2);
    poopEl.style.transform += ` translate(${dx}px, ${dy}px) scale(0.1)`;
    poopEl.style.opacity = '0';
    hasPoop = false;
    setTimeout(() => alert('ミッションクリア！🎉'), 700);
  }
}
