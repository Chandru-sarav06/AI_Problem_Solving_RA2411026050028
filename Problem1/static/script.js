let board = ['', '', '', '', '', '', '', '', ''];
let gameActive = true;
const PLAYER_X = 'X';
const PLAYER_O = 'O';

const cells = document.querySelectorAll('.cell');
const statusDisplay = document.querySelector('#modal-msg');
const execTimeDisplay = document.querySelector('#exec-time');
const nodesCountDisplay = document.querySelector('#nodes-count');
const algorithmSelect = document.querySelector('#algorithm');
const resetBtn = document.querySelector('#reset-btn');
const modal = document.querySelector('#modal');
const modalClose = document.querySelector('#modal-close');

function updateBoardUI() {
    cells.forEach((cell, index) => {
        cell.textContent = board[index];
        cell.className = 'cell'; // Reset classes
        if (board[index] === PLAYER_X) {
            cell.classList.add('x');
        } else if (board[index] === PLAYER_O) {
            cell.classList.add('o');
        }
    });
}

function handleResultValidation(winner) {
    if (winner) {
        gameActive = false;
        if (winner === 'Tie') {
            statusDisplay.textContent = 'Game Ended in a Tie!';
            statusDisplay.style.color = 'var(--text-main)';
        } else {
            statusDisplay.textContent = winner === PLAYER_X ? 'You Win!' : 'AI Wins!';
            statusDisplay.style.color = winner === PLAYER_X ? 'var(--player-x)' : 'var(--player-o)';
        }
        modal.classList.remove('hidden');
    }
}

async function makeAiMove() {
    if (!gameActive) return;
    
    isProcessing = true;
    // Set a loading state
    document.body.style.cursor = 'wait';
    
    const algorithm = algorithmSelect.value;
    
    try {
        const response = await fetch('/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ board, algorithm })
        });
        
        const data = await response.json();
        
        if (data.error) {
            console.error(data.error);
            document.body.style.cursor = 'default';
            isProcessing = false;
            return;
        }

        board = data.board;
        execTimeDisplay.textContent = `${data.execution_time.toFixed(2)} ms`;
        nodesCountDisplay.textContent = data.nodes_explored.toLocaleString();
        
        updateBoardUI();
        handleResultValidation(data.winner);

    } catch (error) {
        console.error('Error making AI move:', error);
    } finally {
        document.body.style.cursor = 'default';
        isProcessing = false;
    }
}

let isProcessing = false;

function handleCellClick(e) {
    const clickedCell = e.target;
    const cellIndex = parseInt(clickedCell.getAttribute('data-index'));

    if (board[cellIndex] !== '' || !gameActive || isProcessing) {
        return;
    }

    board[cellIndex] = PLAYER_X;
    updateBoardUI();
    
    makeAiMove();
}

function resetGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    gameActive = true;
    execTimeDisplay.textContent = '0.00 ms';
    nodesCountDisplay.textContent = '0';
    statusDisplay.style.color = 'var(--text-main)';
    modal.classList.add('hidden');
    updateBoardUI();
}

cells.forEach(cell => cell.addEventListener('click', handleCellClick));
resetBtn.addEventListener('click', resetGame);
modalClose.addEventListener('click', resetGame);

// Initial UI setup
updateBoardUI();
