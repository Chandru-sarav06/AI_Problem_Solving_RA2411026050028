from flask import Flask, request, jsonify, render_template
from game_ai import TicTacToeAI

app = Flask(__name__)
ai = TicTacToeAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    board = data.get('board', [''] * 9)
    algorithm = data.get('algorithm', 'alphabeta')  # 'minimax' or 'alphabeta'
    
    use_alphabeta = (algorithm == 'alphabeta')
    
    # Ensure all user inputs and current board are valid
    if len(board) != 9:
        return jsonify({'error': 'Invalid board'})

    winner = ai.check_winner(board)
    # If the user already won or tie, just return
    if winner:
         return jsonify({'board': board, 'winner': winner, 'execution_time': 0, 'nodes_explored': 0, 'move': -1})

    best_move, execution_time, nodes_explored = ai.get_best_move(board, use_alphabeta)
    
    if best_move != -1:
        board[best_move] = 'O'
        
    winner = ai.check_winner(board)
    
    return jsonify({
        'move': best_move,
        'board': board,
        'execution_time': execution_time,
        'nodes_explored': nodes_explored,
        'winner': winner
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
