# AI Problem Solving Assignment
 
**Team Members: 
		1.CHANDRU M S (RA2411026050028)
		2.Jagan Karthick A (RA2411026050028)

---

## Problems Implemented

### Problem 1 — Interactive Game AI (Tic-Tac-Toe)
### Problem 2 — Disaster Evacuation Planner

---

## Problem 1: Interactive Game AI — Tic-Tac-Toe

### Description
A web-based Tic-Tac-Toe game where the AI always plays optimally. The user can switch between two AI algorithms in real time and compare their performance.

### Algorithms Used

| Algorithm | Description |
|-----------|-------------|
| **Minimax** | Recursively explores all possible game states. Guarantees optimal play but explores every node. |
| **Alpha-Beta Pruning** | Minimax enhanced with pruning — cuts branches that cannot affect the final decision. Explores fewer nodes while producing identical results. |

### Execution Steps
```bash
cd Problem1_TicTacToe
pip install flask
python tictactoe.py
# Open http://localhost:5000
```

### Sample Output
```
Human (X) clicks cell 4 (center)
AI (O) searches using Alpha-Beta:
  Nodes explored: 18
  Time: 0.12 ms
  Best move: corner (cell 0)

vs Minimax:
  Nodes explored: 255
  Time: 0.89 ms
  (same move, more work)
```

### Key Findings
- Alpha-Beta pruning reduces nodes explored by **~70–90%** compared to plain Minimax
- Both algorithms always produce the **same best move** — pruning never changes quality
- At depth 0 (empty board), Minimax explores ~255,168 nodes; Alpha-Beta explores ~~18,297

---

## Problem 2: Disaster Evacuation Planner

### Description
An interactive puzzle where 3 civilians and 3 criminals must cross a river. The constraint is that criminals must never outnumber civilians on either side. The system validates every move, provides hints using BFS, and can auto-solve the puzzle.

### Algorithms Used

| Concept | Implementation |
|---------|---------------|
| **State Space Formulation** | State = (left_civ, left_crim, right_civ, right_crim, boat_side) |
| **BFS Search** | Finds the optimal sequence of moves from any state to the goal |
| **Constraint Validation** | Each state is checked: `criminals ≤ civilians` on both shores (when civilians > 0) |

### Execution Steps
```bash
cd Problem2_Evacuation
pip install flask
python evacuation.py
# Open http://localhost:5001
```

### Sample Output
```
Initial State: Left(3C, 3K) | Right(0C, 0K) | Boat: Left

Step 1: Move 1C + 1K → Right  [Valid]
Step 2: Move 1C → Left        [Valid]
Step 3: Move 2K → Right       [Valid]
...
Step 11: Final — Left(0C, 0K) | Right(3C, 3K) ✓ SOLVED

BFS solution length: 11 steps
States explored: 16
```

### State Space Analysis
- Total valid states: 16
- Solution depth: 11 moves
- BFS guarantees shortest path

---

## Folder Structure
```
AI_ProblemSolving/
├── Problem1_TicTacToe/
│   └── tictactoe.py         # Flask app — Minimax + Alpha-Beta
├── Problem2_Evacuation/
│   └── evacuation.py        # Flask app — BFS State Space Search
└── README.md
```

## Requirements
- Python 3.8+
- Flask (`pip install flask`)
