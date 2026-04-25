# AI Problem Solving Assignment
 
Team Members: 
		1.CHANDRU M S (RA2411026050028)

---

## Problems Implemented

### Problem 1 — Interactive Game AI (Tic-Tac-Toe)
### Problem 2 — GPS-Based City Route Finder (A* Algorithm)
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

## Problem 2: GPS-Based City Route Finder (A* Algorithm)
A navigation system that finds the shortest/fastest path between two locations in a city, similar to Google Maps.
The city is modeled as a graph or grid, where:
	Nodes represent locations
	Edges represent roads with travel costs
	Some paths may be blocked

Users can input the map, start point, and destination via a GUI.

Algorithm Used
A* Search Algorithm
Combines actual cost and heuristic estimate
Efficient and optimal pathfinding- Python 3.8+
- Flask (`pip install flask`)

Core Concept

A* evaluates nodes using:

f(n) = g(n) + h(n)

Where:

g(n) = actual cost from start
h(n) = estimated cost to goal (heuristic)

Execution Steps
cd Problem2_Navigation
pip install flask
python navigation.py

Open browser: http://localhost:5001

Sample Output
Start: A
Goal: G

Optimal Path: A → B → D → G
Total Cost: 12

Nodes Explored: 8
