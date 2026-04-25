import heapq
import re

def parse_graph(graph_str):
    graph = {}
    lines = graph_str.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Strip bullets if user copy pasted
        line = line.lstrip('•').strip()
        line = line.lstrip('*').strip()
        
        # Example format: A -> B (1), C (4)
        parts = line.split('->')
        if len(parts) != 2:
            # Fallback for alternative arrow
            parts = line.split('→')
            if len(parts) != 2:
                continue
        
        node = parts[0].strip()
        graph[node] = {}
        
        neighbors_str = parts[1].strip()
        neighbors = [n.strip() for n in neighbors_str.split(',')]
        for n_str in neighbors:
            match = re.match(r'([A-Za-z0-9_]+)\s*\(\s*(\d+(\.\d+)?)\s*\)', n_str)
            if match:
                n_node = match.group(1)
                cost = float(match.group(2))
                graph[node][n_node] = int(cost) if cost.is_integer() else cost
            else:
                # what if just 'B' with no cost? Assumed cost 1
                if n_str:
                    graph[node][n_str] = 1
                    
    return graph

def parse_heuristics(h_str):
    heuristics = {}
    # Handles: A: 7, B: 6
    matches = re.finditer(r'([A-Za-z0-9_]+)\s*:\s*(\d+(\.\d+)?)', h_str)
    for match in matches:
        val = float(match.group(2))
        heuristics[match.group(1)] = int(val) if val.is_integer() else val
    return heuristics

def a_star_search(graph, heuristics, start, goal):
    if not start or not goal:
        return {"error": "Please provide a valid start and goal node."}
    
    open_set = []
    # Use counter to avoid comparing nodes with identical f&g scores
    counter = 0 
    
    h_start = heuristics.get(start, 0)
    heapq.heappush(open_set, (h_start, 0, counter, start, [start]))
    
    g_scores = {start: 0}
    explored = []
    
    while open_set:
        f, g, _, current, path = heapq.heappop(open_set)
        
        if current not in explored:
            explored.append(current)
            
        if current == goal:
            return {
                "path": path,
                "cost": g,
                "explored": explored
            }
            
        neighbors = graph.get(current, {})
        for neighbor, weight in neighbors.items():
            tentative_g = g + weight
            
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                f_score = tentative_g + heuristics.get(neighbor, 0)
                new_path = list(path)
                new_path.append(neighbor)
                
                counter += 1
                heapq.heappush(open_set, (f_score, tentative_g, counter, neighbor, new_path))
                
    return {"error": "Goal node could not be reached.", "explored": explored}
