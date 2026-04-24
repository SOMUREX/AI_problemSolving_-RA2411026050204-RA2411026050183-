[tictactoe.html](https://github.com/user-attachments/files/27034872/tictactoe.html)[Uploading tictacto<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Tic-Tac-Toe — Minimax vs Alpha-Beta</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0a0f;
    --panel: #111118;
    --border: #1e1e2e;
    --accent1: #00f5ff;
    --accent2: #ff006e;
    --accent3: #7b2fff;
    --text: #e0e0f0;
    --muted: #555577;
    --win: #00ff88;
    --cell-bg: #0d0d18;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-image: radial-gradient(ellipse at 20% 20%, rgba(0,245,255,0.04) 0%, transparent 50%),
                      radial-gradient(ellipse at 80% 80%, rgba(255,0,110,0.04) 0%, transparent 50%);
  }

  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.2rem, 4vw, 2rem);
    font-weight: 900;
    letter-spacing: 0.15em;
    text-align: center;
    margin-bottom: 6px;
    background: linear-gradient(90deg, var(--accent1), var(--accent3), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.2em;
    text-align: center;
    margin-bottom: 20px;
  }

  .main-layout {
    display: flex;
    gap: 18px;
    align-items: flex-start;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
    max-width: 900px;
  }

  /* CONTROLS */
  .controls-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    min-width: 200px;
    max-width: 240px;
    flex: 1;
  }

  .section-label {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: var(--accent1);
    margin-bottom: 10px;
    text-transform: uppercase;
  }

  .mode-btn {
    display: block;
    width: 100%;
    padding: 10px 12px;
    background: var(--cell-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--muted);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    cursor: pointer;
    text-align: left;
    margin-bottom: 8px;
    transition: all 0.2s;
    letter-spacing: 0.05em;
  }

  .mode-btn:hover { border-color: var(--accent3); color: var(--text); }
  .mode-btn.active { border-color: var(--accent1); color: var(--accent1); background: rgba(0,245,255,0.06); }

  .divider { height: 1px; background: var(--border); margin: 14px 0; }

  .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }

  .stat-label { font-size: 0.68rem; color: var(--muted); }
  .stat-val { font-size: 0.78rem; color: var(--accent1); font-family: 'Orbitron', sans-serif; }
  .stat-val.red { color: var(--accent2); }
  .stat-val.purple { color: var(--accent3); }

  .reset-btn {
    width: 100%;
    padding: 10px;
    margin-top: 14px;
    background: transparent;
    border: 1px solid var(--accent2);
    border-radius: 8px;
    color: var(--accent2);
    font-family: 'Orbitron', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    cursor: pointer;
    transition: all 0.2s;
  }
  .reset-btn:hover { background: rgba(255,0,110,0.1); }

  /* BOARD */
  .game-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 14px;
  }

  .status-bar {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    color: var(--text);
    text-align: center;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .status-bar.win { color: var(--win); }
  .status-bar.draw { color: var(--accent3); }
  .status-bar.thinking { color: var(--accent1); }

  .board {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    padding: 10px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    position: relative;
  }

  .cell {
    width: 90px;
    height: 90px;
    background: var(--cell-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    cursor: pointer;
    transition: all 0.15s;
    position: relative;
    overflow: hidden;
  }

  .cell:hover:not(.taken) {
    border-color: var(--accent3);
    background: rgba(123,47,255,0.08);
  }

  .cell.taken { cursor: default; }
  .cell.X { color: var(--accent1); text-shadow: 0 0 20px var(--accent1); }
  .cell.O { color: var(--accent2); text-shadow: 0 0 20px var(--accent2); }
  .cell.win-cell { 
    background: rgba(0,255,136,0.08);
    border-color: var(--win);
    animation: pulse 0.8s ease-in-out infinite alternate;
  }

  @keyframes pulse {
    from { box-shadow: 0 0 0 0 rgba(0,255,136,0.3); }
    to { box-shadow: 0 0 0 8px rgba(0,255,136,0); }
  }

  .cell-appear {
    animation: cellPop 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }

  @keyframes cellPop {
    from { transform: scale(0.4); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }

  /* SCORE */
  .score-row {
    display: flex;
    gap: 10px;
  }

  .score-card {
    padding: 10px 18px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid var(--border);
    background: var(--panel);
    min-width: 80px;
  }

  .score-card .who { font-size: 0.62rem; color: var(--muted); letter-spacing: 0.15em; }
  .score-card .num {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
  }
  .score-card.player .num { color: var(--accent1); }
  .score-card.ai .num { color: var(--accent2); }
  .score-card.draws .num { color: var(--accent3); }

  /* COMPARISON PANEL */
  .compare-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
    min-width: 200px;
    max-width: 240px;
    flex: 1;
  }

  .algo-block {
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid var(--border);
    margin-bottom: 10px;
  }

  .algo-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
  }

  .algo-block.minimax .algo-name { color: var(--accent3); }
  .algo-block.alphabeta .algo-name { color: var(--accent1); }

  .algo-metric { display: flex; justify-content: space-between; font-size: 0.68rem; padding: 3px 0; }
  .algo-metric .key { color: var(--muted); }
  .algo-metric .val { color: var(--text); }
  .algo-metric .val.faster { color: var(--win); }

  .history-log {
    margin-top: 10px;
    max-height: 130px;
    overflow-y: auto;
    font-size: 0.64rem;
    color: var(--muted);
    line-height: 1.8;
  }

  .history-log::-webkit-scrollbar { width: 3px; }
  .history-log::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  .log-entry { border-bottom: 1px solid rgba(255,255,255,0.03); padding: 2px 0; }
  .log-entry span { color: var(--accent1); }
  .log-entry span.red { color: var(--accent2); }

  .thinking-dots::after {
    content: '';
    animation: dots 1s steps(3, end) infinite;
  }
  @keyframes dots {
    0%   { content: '.'; }
    33%  { content: '..'; }
    66%  { content: '...'; }
    100% { content: ''; }
  }

  @media (max-width: 600px) {
    .cell { width: 72px; height: 72px; font-size: 1.8rem; }
    .controls-panel, .compare-panel { max-width: 100%; min-width: 0; width: 100%; }
    .main-layout { flex-direction: column; align-items: center; }
  }
</style>
</head>
<body>

<h1>AI TIC-TAC-TOE</h1>
<p class="subtitle">MINIMAX &nbsp;|&nbsp; ALPHA-BETA PRUNING &nbsp;|&nbsp; COMPARISON</p>

<div class="main-layout">

  <!-- LEFT: Controls -->
  <div class="controls-panel">
    <div class="section-label">AI Algorithm</div>
    <button class="mode-btn active" id="btn-minimax" onclick="setAlgo('minimax')">
      Minimax
    </button>
    <button class="mode-btn" id="btn-alphabeta" onclick="setAlgo('alphabeta')">
      Alpha-Beta Pruning
    </button>

    <div class="divider"></div>
    <div class="section-label">Difficulty</div>
    <button class="mode-btn active" id="btn-hard" onclick="setDepth(9)">Hard (Unbeatable)</button>
    <button class="mode-btn" id="btn-med" onclick="setDepth(3)">Medium</button>
    <button class="mode-btn" id="btn-easy" onclick="setDepth(1)">Easy</button>

    <div class="divider"></div>
    <div class="section-label">Last Move Stats</div>
    <div class="stat-row"><span class="stat-label">Nodes explored</span><span class="stat-val" id="stat-nodes">—</span></div>
    <div class="stat-row"><span class="stat-label">Time (ms)</span><span class="stat-val" id="stat-time">—</span></div>
    <div class="stat-row"><span class="stat-label">Algorithm</span><span class="stat-val purple" id="stat-algo">MINIMAX</span></div>

    <button class="reset-btn" onclick="resetGame()">⟳ RESET GAME</button>
  </div>

  <!-- CENTER: Game -->
  <div class="game-area">
    <div class="score-row">
      <div class="score-card player"><div class="who">YOU (X)</div><div class="num" id="score-x">0</div></div>
      <div class="score-card draws"><div class="who">DRAWS</div><div class="num" id="score-d">0</div></div>
      <div class="score-card ai"><div class="who">AI (O)</div><div class="num" id="score-o">0</div></div>
    </div>

    <div class="status-bar" id="status">YOUR TURN — PLAY X</div>

    <div class="board" id="board">
      <div class="cell" id="c0" onclick="playerMove(0)"></div>
      <div class="cell" id="c1" onclick="playerMove(1)"></div>
      <div class="cell" id="c2" onclick="playerMove(2)"></div>
      <div class="cell" id="c3" onclick="playerMove(3)"></div>
      <div class="cell" id="c4" onclick="playerMove(4)"></div>
      <div class="cell" id="c5" onclick="playerMove(5)"></div>
      <div class="cell" id="c6" onclick="playerMove(6)"></div>
      <div class="cell" id="c7" onclick="playerMove(7)"></div>
      <div class="cell" id="c8" onclick="playerMove(8)"></div>
    </div>
  </div>

  <!-- RIGHT: Comparison Log -->
  <div class="compare-panel">
    <div class="section-label">Algorithm Comparison</div>

    <div class="algo-block minimax">
      <div class="algo-name">⬡ MINIMAX</div>
      <div class="algo-metric"><span class="key">Total nodes</span><span class="val" id="mm-nodes">0</span></div>
      <div class="algo-metric"><span class="key">Total time</span><span class="val" id="mm-time">0ms</span></div>
      <div class="algo-metric"><span class="key">Moves made</span><span class="val" id="mm-moves">0</span></div>
    </div>

    <div class="algo-block alphabeta">
      <div class="algo-name">⬡ ALPHA-BETA</div>
      <div class="algo-metric"><span class="key">Total nodes</span><span class="val" id="ab-nodes">0</span></div>
      <div class="algo-metric"><span class="key">Total time</span><span class="val" id="ab-time">0ms</span></div>
      <div class="algo-metric"><span class="key">Moves made</span><span class="val" id="ab-moves">0</span></div>
    </div>

    <div class="algo-metric" style="margin-top:4px; font-size:0.66rem; padding: 6px 0;">
      <span class="key">Node reduction</span>
      <span class="val faster" id="reduction">—</span>
    </div>

    <div class="divider"></div>
    <div class="section-label">Move History</div>
    <div class="history-log" id="history-log"></div>
  </div>
</div>

<script>
// ─── State ───────────────────────────────────────────────────────────────────
let board = Array(9).fill(null);
let gameOver = false;
let currentAlgo = 'minimax';
let maxDepth = 9;
let scores = { X: 0, O: 0, D: 0 };
let stats = {
  minimax: { nodes: 0, time: 0, moves: 0 },
  alphabeta: { nodes: 0, time: 0, moves: 0 }
};
let nodeCount = 0;
const WINS = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];

// ─── Helpers ─────────────────────────────────────────────────────────────────
function checkWinner(b) {
  for (let [a,c,d] of WINS)
    if (b[a] && b[a] === b[c] && b[a] === b[d]) return { winner: b[a], line: [a,c,d] };
  if (b.every(x => x)) return { winner: 'draw', line: [] };
  return null;
}

// ─── Minimax ─────────────────────────────────────────────────────────────────
function minimax(b, depth, isMax) {
  nodeCount++;
  const r = checkWinner(b);
  if (r) {
    if (r.winner === 'O') return 10 - (9 - depth);
    if (r.winner === 'X') return -10 + (9 - depth);
    return 0;
  }
  if (depth === 0) return 0;

  if (isMax) {
    let best = -Infinity;
    for (let i = 0; i < 9; i++) {
      if (!b[i]) {
        b[i] = 'O';
        best = Math.max(best, minimax(b, depth - 1, false));
        b[i] = null;
      }
    }
    return best;
  } else {
    let best = Infinity;
    for (let i = 0; i < 9; i++) {
      if (!b[i]) {
        b[i] = 'X';
        best = Math.min(best, minimax(b, depth - 1, true));
        b[i] = null;
      }
    }
    return best;
  }
}

// ─── Alpha-Beta ──────────────────────────────────────────────────────────────
function alphabeta(b, depth, alpha, beta, isMax) {
  nodeCount++;
  const r = checkWinner(b);
  if (r) {
    if (r.winner === 'O') return 10 - (9 - depth);
    if (r.winner === 'X') return -10 + (9 - depth);
    return 0;
  }
  if (depth === 0) return 0;

  if (isMax) {
    let best = -Infinity;
    for (let i = 0; i < 9; i++) {
      if (!b[i]) {
        b[i] = 'O';
        best = Math.max(best, alphabeta(b, depth - 1, alpha, beta, false));
        b[i] = null;
        alpha = Math.max(alpha, best);
        if (beta <= alpha) break;
      }
    }
    return best;
  } else {
    let best = Infinity;
    for (let i = 0; i < 9; i++) {
      if (!b[i]) {
        b[i] = 'X';
        best = Math.min(best, alphabeta(b, depth - 1, alpha, beta, true));
        b[i] = null;
        beta = Math.min(beta, best);
        if (beta <= alpha) break;
      }
    }
    return best;
  }
}

// ─── Best Move ───────────────────────────────────────────────────────────────
function getBestMove(b, algo) {
  nodeCount = 0;
  const t0 = performance.now();
  let bestVal = -Infinity, bestMove = -1;

  for (let i = 0; i < 9; i++) {
    if (!b[i]) {
      b[i] = 'O';
      const val = algo === 'alphabeta'
        ? alphabeta(b, maxDepth, -Infinity, Infinity, false)
        : minimax(b, maxDepth, false);
      b[i] = null;
      if (val > bestVal) { bestVal = val; bestMove = i; }
    }
  }

  const elapsed = +(performance.now() - t0).toFixed(2);

  // Also run OTHER algo for comparison
  const otherAlgo = algo === 'minimax' ? 'alphabeta' : 'minimax';
  const otherNodesBefore = nodeCount;
  nodeCount = 0;
  const t1 = performance.now();
  for (let i = 0; i < 9; i++) {
    if (!b[i]) {
      b[i] = 'O';
      otherAlgo === 'alphabeta'
        ? alphabeta(b, maxDepth, -Infinity, Infinity, false)
        : minimax(b, maxDepth, false);
      b[i] = null;
    }
  }
  const otherNodes = nodeCount;
  const otherTime = +(performance.now() - t1).toFixed(2);
  nodeCount = otherNodesBefore; // restore main

  // Reset nodeCount to current algo's count
  nodeCount = 0;
  const t2 = performance.now();
  for (let i = 0; i < 9; i++) {
    if (!b[i]) {
      b[i] = 'O';
      algo === 'alphabeta'
        ? alphabeta(b, maxDepth, -Infinity, Infinity, false)
        : minimax(b, maxDepth, false);
      b[i] = null;
    }
  }
  const finalNodes = nodeCount;
  const finalTime = +(performance.now() - t2).toFixed(2);

  const curStats  = { nodes: finalNodes, time: finalTime };
  const otherStats= { nodes: otherNodes, time: otherTime };

  if (algo === 'minimax') {
    stats.minimax.nodes += finalNodes; stats.minimax.time += finalTime; stats.minimax.moves++;
    stats.alphabeta.nodes += otherNodes; stats.alphabeta.time += otherTime; stats.alphabeta.moves++;
  } else {
    stats.alphabeta.nodes += finalNodes; stats.alphabeta.time += finalTime; stats.alphabeta.moves++;
    stats.minimax.nodes += otherNodes; stats.minimax.time += otherTime; stats.minimax.moves++;
  }

  return { move: bestMove, nodes: finalNodes, time: finalTime };
}

// ─── Game Logic ──────────────────────────────────────────────────────────────
function playerMove(idx) {
  if (gameOver || board[idx]) return;
  board[idx] = 'X';
  renderCell(idx, 'X');

  const res = checkWinner(board);
  if (res) { endGame(res); return; }

  lockBoard(true);
  setStatus('AI THINKING<span class="thinking-dots"></span>', 'thinking');

  setTimeout(() => {
    const { move, nodes, time } = getBestMove([...board], currentAlgo);
    board[move] = 'O';
    renderCell(move, 'O');
    lockBoard(false);

    document.getElementById('stat-nodes').textContent = nodes.toLocaleString();
    document.getElementById('stat-time').textContent = time + 'ms';
    document.getElementById('stat-algo').textContent = currentAlgo.toUpperCase();
    updateComparePanel();
    addLog(idx, move, nodes, time);

    const res2 = checkWinner(board);
    if (res2) endGame(res2);
    else setStatus('YOUR TURN — PLAY X', '');
  }, 80);
}

function renderCell(idx, player) {
  const el = document.getElementById('c' + idx);
  el.textContent = player;
  el.classList.add('taken', player, 'cell-appear');
}

function endGame(res) {
  gameOver = true;
  if (res.winner === 'X') {
    scores.X++;
    document.getElementById('score-x').textContent = scores.X;
    setStatus('🎉 YOU WIN!', 'win');
  } else if (res.winner === 'O') {
    scores.O++;
    document.getElementById('score-o').textContent = scores.O;
    setStatus('🤖 AI WINS!', 'win');
  } else {
    scores.D++;
    document.getElementById('score-d').textContent = scores.D;
    setStatus('🤝 DRAW!', 'draw');
  }
  if (res.line) res.line.forEach(i => document.getElementById('c' + i).classList.add('win-cell'));
}

function setStatus(html, cls) {
  const el = document.getElementById('status');
  el.innerHTML = html;
  el.className = 'status-bar ' + cls;
}

function lockBoard(lock) {
  for (let i = 0; i < 9; i++) {
    const el = document.getElementById('c' + i);
    if (!board[i]) el.style.pointerEvents = lock ? 'none' : 'auto';
  }
}

function resetGame() {
  board = Array(9).fill(null);
  gameOver = false;
  for (let i = 0; i < 9; i++) {
    const el = document.getElementById('c' + i);
    el.textContent = '';
    el.className = 'cell';
  }
  setStatus('YOUR TURN — PLAY X', '');
  document.getElementById('stat-nodes').textContent = '—';
  document.getElementById('stat-time').textContent = '—';
}

function setAlgo(algo) {
  currentAlgo = algo;
  document.querySelectorAll('#btn-minimax,#btn-alphabeta').forEach(b => b.classList.remove('active'));
  document.getElementById('btn-' + algo).classList.add('active');
  resetGame();
}

function setDepth(d) {
  maxDepth = d;
  document.querySelectorAll('#btn-hard,#btn-med,#btn-easy').forEach(b => b.classList.remove('active'));
  const map = { 9: 'hard', 3: 'med', 1: 'easy' };
  document.getElementById('btn-' + map[d]).classList.add('active');
  resetGame();
}

function updateComparePanel() {
  const mm = stats.minimax, ab = stats.alphabeta;
  document.getElementById('mm-nodes').textContent = mm.nodes.toLocaleString();
  document.getElementById('mm-time').textContent = mm.time.toFixed(1) + 'ms';
  document.getElementById('mm-moves').textContent = mm.moves;
  document.getElementById('ab-nodes').textContent = ab.nodes.toLocaleString();
  document.getElementById('ab-time').textContent = ab.time.toFixed(1) + 'ms';
  document.getElementById('ab-moves').textContent = ab.moves;

  if (mm.nodes > 0 && ab.nodes > 0) {
    const pct = Math.round((1 - ab.nodes / mm.nodes) * 100);
    document.getElementById('reduction').textContent =
      pct > 0 ? `AB saves ${pct}% nodes` : 'Similar efficiency';
  }
}

function addLog(playerIdx, aiIdx, nodes, time) {
  const log = document.getElementById('history-log');
  const row = document.createElement('div');
  row.className = 'log-entry';
  row.innerHTML = `You→<span>pos${playerIdx}</span> AI→<span class="red">pos${aiIdx}</span> [${nodes}n, ${time}ms]`;
  log.prepend(row);
}
</script>
</body>
</html>
e.html…]()
