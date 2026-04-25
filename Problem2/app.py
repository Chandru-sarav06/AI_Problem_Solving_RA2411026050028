from flask import Flask, render_template, request, jsonify
from astar import parse_graph, parse_heuristics, a_star_search

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    graph_str = data.get('graph', '')
    heuristic_str = data.get('heuristics', '')
    start_node = data.get('start', '').strip()
    goal_node = data.get('goal', '').strip()
    
    graph = parse_graph(graph_str)
    heuristics = parse_heuristics(heuristic_str)
    
    result = a_star_search(graph, heuristics, start_node, goal_node)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
