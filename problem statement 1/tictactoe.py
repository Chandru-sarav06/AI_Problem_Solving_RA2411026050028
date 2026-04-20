"""
Problem 1: Interactive Game AI — Tic-Tac-Toe
Algorithm: Minimax + Alpha-Beta Pruning
Requires: pip install flask
Run: python tictactoe.py  → open http://localhost:5000
"""

import time
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return 'draw'
    return None

# ── Minimax (no pruning) ────────────────────────────────────────────
def minimax(board, is_max, ai, human, depth=0):
    winner = check_winner(board)
    if winner == ai:     return 10 - depth, 1
    if winner == human:  return depth - 10, 1
    if winner == 'draw': return 0, 1

    best = -100 if is_max else 100
    total_nodes = 1
    for i in range(9):
        if board[i] is None:
            board[i] = ai if is_max else human
            score, nodes = minimax(board, not is_max, ai, human, depth + 1)
            board[i] = None
            total_nodes += nodes
            if is_max and score > best: best = score
            if not is_max and score < best: best = score
    return best, total_nodes

# ── Alpha-Beta Pruning ──────────────────────────────────────────────
def alphabeta(board, is_max, ai, human, depth=0, alpha=-1000, beta=1000):
    winner = check_winner(board)
    if winner == ai:     return 10 - depth, 1
    if winner == human:  return depth - 10, 1
    if winner == 'draw': return 0, 1

    best = -100 if is_max else 100
    total_nodes = 1
    for i in range(9):
        if board[i] is None:
            board[i] = ai if is_max else human
            score, nodes = alphabeta(board, not is_max, ai, human, depth + 1, alpha, beta)
            board[i] = None
            total_nodes += nodes
            if is_max:
                if score > best: best = score
                if best > alpha: alpha = best
            else:
                if score < best: best = score
                if best < beta: beta = best
            if alpha >= beta:
                break
    return best, total_nodes

# ── Best move ───────────────────────────────────────────────────────
def get_best_move(board, ai, human, use_alphabeta=False):
    best_score, best_idx, total_nodes = -1000, -1, 0
    t0 = time.perf_counter()
    for i in range(9):
        if board[i] is None:
            board[i] = ai
            if use_alphabeta:
                score, nodes = alphabeta(board, False, ai, human)
            else:
                score, nodes = minimax(board, False, ai, human)
            board[i] = None
            total_nodes += nodes
            if score > best_score:
                best_score, best_idx = score, i
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 3)
    return best_idx, total_nodes, elapsed_ms

# ── Flask routes ────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/ai_move', methods=['POST'])
def ai_move():
    data = request.json
    board = data['board']          # list of 9, values: 'X','O', or None
    ai    = data['ai']             # 'X' or 'O'
    human = 'O' if ai == 'X' else 'X'
    algo  = data.get('algo', 'minimax')

    move, nodes, ms = get_best_move(board, ai, human, use_alphabeta=(algo=='alphabeta'))
    if move >= 0:
        board[move] = ai
    winner = check_winner(board)
    return jsonify({'move': move, 'board': board, 'winner': winner,
                    'nodes': nodes, 'time_ms': ms})

# ── Embedded HTML (single-file deployment) ─────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Tic-Tac-Toe AI</title>
<style>
  body{font-family:Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:30px;background:#f5f5f5}
  h1{margin-bottom:4px}
  .controls{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin:14px 0}
  .board{display:grid;grid-template-columns:repeat(3,100px);gap:6px;margin:16px 0}
  .cell{width:100px;height:100px;background:#fff;border:2px solid #ccc;border-radius:8px;font-size:42px;font-weight:bold;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .1s}
  .cell:hover:not(.taken){background:#e8f4ff}
  .cell.taken{cursor:default}.cell.X{color:#1a6fba}.cell.O{color:#b83030}
  .cell.win{background:#c8f0c8}
  .status{font-size:18px;font-weight:bold;min-height:26px;margin:8px 0}
  .metrics{display:flex;gap:20px;flex-wrap:wrap;justify-content:center;margin:12px 0}
  .metric{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px 18px;text-align:center}
  .metric-label{font-size:11px;color:#888;margin-bottom:4px}
  .metric-val{font-size:22px;font-weight:bold}
  table{border-collapse:collapse;font-size:13px;margin-top:10px}
  th,td{border:1px solid #ddd;padding:7px 14px;text-align:left}
  th{background:#f0f0f0}
  button,select{font-size:13px;padding:6px 14px;border-radius:6px;border:1px solid #ccc;cursor:pointer}
  button{background:#fff} button:hover{background:#e8f4ff}
</style>
</head>
<body>
<h1>Tic-Tac-Toe AI</h1>
<p style="color:#666;margin-bottom:6px">Minimax vs Alpha-Beta Pruning — Performance Comparison</p>

<div class="controls">
  <label>Algorithm:
    <select id="algo">
      <option value="minimax">Minimax</option>
      <option value="alphabeta">Alpha-Beta Pruning</option>
    </select>
  </label>
  <label>You play as:
    <select id="human-side">
      <option value="X">X (first)</option>
      <option value="O">O (second)</option>
    </select>
  </label>
  <button onclick="resetGame()">↺ Reset</button>
</div>

<div class="board" id="board">
  <div class="cell" onclick="humanMove(0)"></div><div class="cell" onclick="humanMove(1)"></div><div class="cell" onclick="humanMove(2)"></div>
  <div class="cell" onclick="humanMove(3)"></div><div class="cell" onclick="humanMove(4)"></div><div class="cell" onclick="humanMove(5)"></div>
  <div class="cell" onclick="humanMove(6)"></div><div class="cell" onclick="humanMove(7)"></div><div class="cell" onclick="humanMove(8)"></div>
</div>

<div class="status" id="status">Your turn</div>

<div class="metrics">
  <div class="metric"><div class="metric-label">Nodes explored</div><div class="metric-val" id="m-nodes">—</div></div>
  <div class="metric"><div class="metric-label">Time (ms)</div><div class="metric-val" id="m-time">—</div></div>
</div>

<div style="font-weight:bold;margin:12px 0 4px">Session Comparison</div>
<table>
  <tr><th>Algorithm</th><th>Avg Nodes</th><th>Avg Time (ms)</th><th>Pruning</th></tr>
  <tr><td>Minimax</td><td id="c-mm-n">—</td><td id="c-mm-t">—</td><td>❌ None</td></tr>
  <tr><td>Alpha-Beta</td><td id="c-ab-n">—</td><td id="c-ab-t">—</td><td>✅ Yes</td></tr>
</table>

<script>
let board = Array(9).fill(null), active = true;
let cmp = {minimax:{n:[],t:[]}, alphabeta:{n:[],t:[]}};
const WIN_LINES = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];

function human(){ return document.getElementById('human-side').value; }
function ai(){ return human()==='X'?'O':'X'; }
function algo(){ return document.getElementById('algo').value; }

function renderBoard(winLine){
  document.querySelectorAll('.cell').forEach((c,i)=>{
    c.textContent = board[i]||'';
    c.className = 'cell'+(board[i]?' taken '+board[i]:'');
    if(winLine&&winLine.includes(i)) c.classList.add('win');
  });
}

function checkWinner(b){
  for(let [a,bc,c] of WIN_LINES) if(b[a]&&b[a]===b[bc]&&b[a]===b[c]) return b[a];
  return b.every(x=>x)?'draw':null;
}

async function humanMove(i){
  if(!active||board[i]) return;
  board[i] = human();
  renderBoard();
  let w = checkWinner(board);
  if(w){ endGame(w); return; }
  document.getElementById('status').textContent = 'AI thinking…';
  const res = await fetch('/ai_move',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({board:[...board],ai:ai(),algo:algo()})});
  const data = await res.json();
  board = data.board;
  document.getElementById('m-nodes').textContent = data.nodes;
  document.getElementById('m-time').textContent = data.time_ms;
  cmp[algo()].n.push(data.nodes); cmp[algo()].t.push(data.time_ms);
  updateCompare();
  let wl = WIN_LINES.find(l=>l.every(x=>board[x]===ai()));
  renderBoard(data.winner&&data.winner!=='draw'?wl:null);
  if(data.winner){ endGame(data.winner); return; }
  document.getElementById('status').textContent = 'Your turn';
}

function endGame(w){
  active = false;
  document.getElementById('status').textContent = w==='draw'?'Draw! 🤝':w===human()?'You win! 🎉':'AI wins! 🤖';
}

function updateCompare(){
  ['minimax','alphabeta'].forEach(k=>{
    let s = k==='minimax'?'mm':'ab';
    let d = cmp[k];
    if(!d.n.length) return;
    document.getElementById('c-'+s+'-n').textContent = Math.round(d.n.reduce((a,b)=>a+b)/d.n.length);
    document.getElementById('c-'+s+'-t').textContent = (d.t.reduce((a,b)=>a+b)/d.t.length).toFixed(2);
  });
}

function resetGame(){
  board = Array(9).fill(null); active = true;
  document.getElementById('m-nodes').textContent='—';
  document.getElementById('m-time').textContent='—';
  document.getElementById('status').textContent='Your turn';
  renderBoard();
  if(human()==='O'){
    document.getElementById('status').textContent='AI goes first…';
    setTimeout(()=>humanMove(-1),200);
  }
}

document.getElementById('human-side').onchange = resetGame;
document.getElementById('algo').onchange = resetGame;
</script>
</body>
</html>
"""

if __name__ == '__main__':
    print("Starting Tic-Tac-Toe AI server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
