const calculateBtn = document.getElementById('calculate-btn');
const resultsContainer = document.getElementById('results-container');
const graphInput = document.getElementById('graph-input');
const heuristicInput = document.getElementById('heuristic-input');
const startNode = document.getElementById('start-node');
const goalNode = document.getElementById('goal-node');

// Pre-fill sample data
graphInput.value = `A → B (1), C (4)
B → D (2), E (5)
C → D (1)
D → F (3)
E → F (1)`;

heuristicInput.value = `A: 7, B: 6, C: 4, D: 2, E: 1, F: 0`;

calculateBtn.addEventListener('click', async () => {
    const graph = graphInput.value.trim();
    const heuristics = heuristicInput.value.trim();
    const start = startNode.value.trim();
    const goal = goalNode.value.trim();

    if (!graph || !start || !goal) {
        showError('Please fill in the city map, start, and destination fields.');
        return;
    }

    calculateBtn.disabled = true;
    calculateBtn.innerHTML = `<svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg> Calculating...`;

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ graph, heuristics, start, goal })
        });

        const data = await response.json();

        if (data.error) {
            showError(data.error, data.explored);
        } else {
            showResults(data, start, goal);
        }
    } catch (err) {
        showError('Failed to connect to the server. Is the Flask app running?');
    } finally {
        calculateBtn.disabled = false;
        calculateBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg> Calculate Optimal Route`;
    }
});

function showResults(data, start, goal) {
    const path = data.path;
    const cost = data.cost;
    const explored = data.explored;

    // Build path visualization with arrows + animated path nodes
    const pathHTML = path.map((node, idx) => {
        const isFirst = idx === 0;
        const isLast = idx === path.length - 1;
        const label = isFirst ? `${node} (Start)` : isLast ? `${node} (Goal)` : node;
        const arrow = idx < path.length - 1 ? `<span class="arrow">→</span>` : '';
        return `<span class="node path-node" style="animation-delay: ${idx * 0.1}s">${label}</span>${arrow}`;
    }).join('');

    // Build cost breakdown
    const costBreakdown = path.length > 1
        ? path.slice(1).map((node, idx) => `<code>${path[idx]} → ${node}</code>`).join(' + ') + ` = <strong>${cost}</strong>`
        : `<strong>${cost}</strong>`;

    resultsContainer.innerHTML = `
        <div class="result-content">
            <div class="metrics">
                <div class="metric-box">
                    <div class="metric-label">Total Cost</div>
                    <div class="metric-val">${cost}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Path Length</div>
                    <div class="metric-val">${path.length - 1} <small style="font-size:1rem">hops</small></div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Nodes Explored</div>
                    <div class="metric-val">${explored.length}</div>
                </div>
            </div>

            <div class="path-visualizer">
                <div class="path-title">✅ Optimal Path — A* Result</div>
                <div class="nodes-row">${pathHTML}</div>
            </div>

            <div class="path-visualizer">
                <div class="path-title">💰 Cost Breakdown</div>
                <div class="explored-list">${costBreakdown}</div>
            </div>

            <div class="path-visualizer">
                <div class="path-title">🔍 Nodes Explored (Search Order)</div>
                <div class="explored-list">${explored.join('  →  ')}</div>
            </div>
        </div>
    `;
}

function showError(message, explored) {
    let exploredHTML = '';
    if (explored && explored.length) {
        exploredHTML = `
            <div class="path-visualizer" style="margin-top: 1.5rem;">
                <div class="path-title">🔍 Nodes Explored Before Failure</div>
                <div class="explored-list">${explored.join('  →  ')}</div>
            </div>`;
    }

    resultsContainer.innerHTML = `
        <div class="error-msg">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            ${message}
        </div>
        ${exploredHTML}
    `;
}
