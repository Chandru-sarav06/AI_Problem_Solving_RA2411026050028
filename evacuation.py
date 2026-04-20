"""
Problem 2: Disaster Evacuation Planner
Similar to Missionaries & Cannibals problem.
Algorithm: BFS-based State Space Search with constraint validation
Requires: pip install flask
Run: python evacuation.py  → open http://localhost:5001
"""

from collections import deque
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ── State representation ────────────────────────────────────────────
# State: (left_civ, left_crim, right_civ, right_crim, boat_side)
# boat_side: 0 = left, 1 = right
INITIAL = (3, 3, 0, 0, 0)
GOAL    = (0, 0, 3, 3, 1)

def is_valid(state):
    lc, lk, rc, rk, _ = state
    if lc < 0 or lk < 0 or rc < 0 or rk < 0: return False
    if lc > 3 or lk > 3 or rc > 3 or rk > 3: return False
    # Criminals must not outnumber civilians (unless 0 civilians on that side)
    if lc > 0 and lk > lc: return False
    if rc > 0 and rk > rc: return False
    return True

def get_successors(state):
    lc, lk, rc, rk, boat = state
    moves = []
    for civ in range(3):
        for crim in range(3 - civ):
            if civ + crim < 1 or civ + crim > 2:
                continue
            if boat == 0:   # move left → right
                ns = (lc - civ, lk - crim, rc + civ, rk + crim, 1)
            else:           # move right → left
                ns = (lc + civ, lk + crim, rc - civ, rk - crim, 0)
            if is_valid(ns):
                moves.append((ns, civ, crim))
    return moves

def bfs_solve(start=INITIAL):
    """Returns list of (state, civ_moved, crim_moved) from start → goal."""
    queue = deque([(start, [])])
    visited = {start}
    while queue:
        state, path = queue.popleft()
        if state == GOAL:
            return path
        for ns, cv, cr in get_successors(state):
            if ns not in visited:
                visited.add(ns)
                queue.append((ns, path + [(ns, cv, cr)]))
    return None

def get_hint(state_tuple):
    """Run BFS from current state and return the next best move."""
    solution = bfs_solve(tuple(state_tuple))
    if not solution:
        return None
    next_state, civ, crim = solution[0]
    boat = state_tuple[4]
    direction = "left → right" if boat == 0 else "right → left"
    return {"civ": civ, "crim": crim, "direction": direction}

# ── Flask routes ────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    state = tuple(data['state'])       # (lc, lk, rc, rk, boat)
    civ   = data['civ']
    crim  = data['crim']
    lc, lk, rc, rk, boat = state

    if boat == 0:
        ns = (lc - civ, lk - crim, rc + civ, rk + crim, 1)
    else:
        ns = (lc + civ, lk + crim, rc - civ, rk - crim, 0)

    if not is_valid(ns):
        return jsonify({'ok': False, 'error': 'Invalid move: criminals would outnumber civilians!'})

    won = list(ns) == list(GOAL)
    return jsonify({'ok': True, 'state': list(ns), 'won': won})

@app.route('/hint', methods=['POST'])
def hint():
    state = tuple(request.json['state'])
    h = get_hint(state)
    if not h:
        return jsonify({'hint': 'No solution from this state!'})
    return jsonify({'hint': f"Move {h['civ']} civilian(s) + {h['crim']} criminal(s) {h['direction']}"})

@app.route('/solve', methods=['POST'])
def solve():
    state = tuple(request.json['state'])
    solution = bfs_solve(state)
    if not solution:
        return jsonify({'steps': []})
    steps = []
    for ns, civ, crim in solution:
        steps.append({'state': list(ns), 'civ': civ, 'crim': crim})
    return jsonify({'steps': steps})

# ── Embedded HTML ───────────────────────────────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Disaster Evacuation Planner</title>
<style>
  body{font-family:Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:24px;background:#f5f7fa}
  h1{margin-bottom:4px}
  .scene{display:flex;gap:0;width:600px;min-height:140px;margin:16px 0;border-radius:10px;overflow:hidden}
  .shore{flex:1;background:#e8f4e8;border:1px solid #aad4aa;padding:12px}
  .river{width:50px;background:#b5d4f4;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:11px;color:#185fa5;font-weight:bold;gap:2px}
  .shore-title{font-size:11px;font-weight:bold;text-transform:uppercase;color:#555;margin-bottom:8px}
  .person{display:inline-block;padding:3px 8px;border-radius:5px;margin:2px;font-size:13px;font-weight:bold;cursor:pointer;user-select:none}
  .civ{background:#dbeafe;color:#1a6fba;border:1px solid #93c5fd}
  .crim{background:#fee2e2;color:#b83030;border:1px solid #fca5a5}
  .person.sel{outline:2px solid #333;outline-offset:1px}
  .boat-box{background:#fef3c7;border:1px solid #fbbf24;border-radius:8px;padding:10px 16px;margin:4px 0 10px;text-align:center;width:300px}
  .boat-label{font-size:11px;font-weight:bold;color:#92400e;margin-bottom:4px}
  .controls{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:12px}
  button{font-size:13px;padding:6px 16px;border-radius:6px;border:1px solid #ccc;cursor:pointer;background:#fff}
  button:hover{background:#e8f4ff}
  .log{width:560px;max-height:120px;overflow-y:auto;background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px;font-size:12px;margin-top:8px}
  .log p{margin:2px 0}.log .ok{color:#166534}.log .err{color:#b83030}.log .tip{color:#1a6fba}
  .state-bar{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:8px 0;font-size:13px}
  .state-chip{background:#fff;border:1px solid #ddd;border-radius:6px;padding:5px 12px}
</style>
</head>
<body>
<h1>Disaster Evacuation Planner</h1>
<p style="color:#555;margin-bottom:6px">Move 3 civilians (C) and 3 criminals (K) across — criminals must never outnumber civilians on either side.</p>

<div class="state-bar" id="state-bar"></div>
<div class="scene" id="scene"></div>

<div class="boat-box">
  <div class="boat-label">BOAT — select people from the boat's side, then cross</div>
  <div id="boat-display" style="min-height:22px;font-size:12px"></div>
</div>

<div class="controls">
  <button onclick="cross()">⛵ Cross river</button>
  <button onclick="clearSel()">✕ Clear</button>
  <button onclick="getHint()">💡 Hint</button>
  <button onclick="autoSolve()">🤖 Auto solve (BFS)</button>
  <button onclick="resetGame()">↺ Reset</button>
</div>

<div class="log" id="log"><p class="tip">Select 1–2 people from the shore where the boat is, then click "Cross river".</p></div>

<script>
let state = [3,3,0,0,0]; // lc,lk,rc,rk,boat
let selected = [];

function render(){
  let [lc,lk,rc,rk,boat] = state;
  let sceneHTML = `
    <div class="shore">
      <div class="shore-title">Left shore ${boat===0?'⛵':''} — Civ:${lc} Crim:${lk}</div>
      ${makePeople('left', lc, lk)}
    </div>
    <div class="river">
      <span style="font-size:20px">${boat===0?'⛵':''}</span>
      <span>~RIVER~</span>
      <span style="font-size:20px">${boat===1?'⛵':''}</span>
    </div>
    <div class="shore">
      <div class="shore-title">${boat===1?'⛵':''} Right shore — Civ:${rc} Crim:${rk}</div>
      ${makePeople('right', rc, rk)}
    </div>`;
  document.getElementById('scene').innerHTML = sceneHTML;

  let barHTML = `
    <div class="state-chip"><b>Left:</b> ${lc} civilians, ${lk} criminals</div>
    <div class="state-chip"><b>Right:</b> ${rc} civilians, ${rk} criminals</div>
    <div class="state-chip"><b>Boat:</b> ${boat===0?'left':'right'} side</div>`;
  document.getElementById('state-bar').innerHTML = barHTML;

  let civSel = selected.filter(x=>x.type==='civ').length;
  let kSel = selected.filter(x=>x.type==='crim').length;
  let boat_html = !selected.length ? '<span style="color:#aaa">nothing selected</span>' :
    '<span class="person civ">C</span>'.repeat(civSel) + '<span class="person crim">K</span>'.repeat(kSel);
  document.getElementById('boat-display').innerHTML = boat_html;
}

function makePeople(side, civ, crim){
  let [lc,lk,rc,rk,boat] = state;
  let onThisSide = side==='left'?boat===0:boat===1;
  let civSel = selected.filter(x=>x.type==='civ'&&x.side===side).length;
  let crimSel = selected.filter(x=>x.type==='crim'&&x.side===side).length;
  let h = '';
  for(let i=0;i<civ;i++){
    let s = i<civSel?' sel':'';
    h += `<span class="person civ${s}" onclick="toggleSel('${side}','civ',${i})">C${i+1}</span>`;
  }
  for(let i=0;i<crim;i++){
    let s = i<crimSel?' sel':'';
    h += `<span class="person crim${s}" onclick="toggleSel('${side}','crim',${i})">K${i+1}</span>`;
  }
  return h || '<span style="font-size:11px;color:#aaa">empty</span>';
}

function toggleSel(side, type, idx){
  let [lc,lk,rc,rk,boat] = state;
  let boatSide = boat===0?'left':'right';
  if(side !== boatSide){ addLog('Boat is on the other side!','err'); return; }
  let existing = selected.findIndex(x=>x.side===side&&x.type===type&&x.idx===idx);
  if(existing>=0){ selected.splice(existing,1); }
  else {
    if(selected.length>=2){ addLog('Boat holds max 2 people.','err'); return; }
    selected.push({side,type,idx});
  }
  render();
}

function clearSel(){ selected=[]; render(); }

async function cross(){
  if(!selected.length){ addLog('Select at least 1 person.','err'); return; }
  let civ = selected.filter(x=>x.type==='civ').length;
  let crim = selected.filter(x=>x.type==='crim').length;
  const res = await fetch('/move',{method:'POST',headers:{'Content-Type':'application/json'},
    body: JSON.stringify({state, civ, crim})});
  const data = await res.json();
  if(!data.ok){ addLog(data.error,'err'); return; }
  state = data.state; selected = [];
  addLog(`Moved ${civ} civilian(s) + ${crim} criminal(s) → ${state[4]===1?'right':'left'} shore`,'ok');
  render();
  if(data.won) addLog('🎉 All evacuated successfully! Puzzle solved!','ok');
}

async function getHint(){
  const res = await fetch('/hint',{method:'POST',headers:{'Content-Type':'application/json'},
    body: JSON.stringify({state})});
  const data = await res.json();
  addLog('💡 ' + data.hint, 'tip');
}

async function autoSolve(){
  const res = await fetch('/solve',{method:'POST',headers:{'Content-Type':'application/json'},
    body: JSON.stringify({state})});
  const data = await res.json();
  if(!data.steps.length){ addLog('Already solved or no solution!','err'); return; }
  addLog(`BFS found solution in ${data.steps.length} steps. Auto-playing...`,'tip');
  for(let step of data.steps){
    await new Promise(r=>setTimeout(r,800));
    state = step.state; selected = [];
    addLog(`Move ${step.civ} civ + ${step.crim} crim`, 'ok');
    render();
  }
  if(JSON.stringify(state)===JSON.stringify([0,0,3,3,1])){
    addLog('🎉 All evacuated!','ok');
  }
}

function addLog(msg, cls){
  let log = document.getElementById('log');
  log.innerHTML += `<p class="${cls||''}">${msg}</p>`;
  log.scrollTop = log.scrollHeight;
}

function resetGame(){
  state=[3,3,0,0,0]; selected=[];
  document.getElementById('log').innerHTML='<p class="tip">Select 1–2 people from the shore where the boat is, then click Cross river. Civilians=C, Criminals=K.</p>';
  render();
}

render();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    print("Starting Evacuation Planner server...")
    print("Open http://localhost:5001 in your browser")
    app.run(debug=True, port=5001)
