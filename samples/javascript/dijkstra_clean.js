/**
 * Initializes distance mapping for all graph nodes.
 *
 * @param {Record<string, Record<string, number>>} [graph={}] - Graph nodes.
 * @param {string} [startNode=''] - Starting vertex.
 * @returns {Record<string, number>} Initial distances.
 */
function initDistances(graph = {}, startNode = '') {
    const distances = {};
    for (const node of Object.keys(graph)) {
        distances[node] = Infinity;
    }
    distances[startNode] = 0;
    return distances;
}

/**
 * Finds the unvisited vertex with the minimal accumulated distance.
 *
 * @param {Record<string, number>} [distances={}] - Current distance table.
 * @param {Set<string>} [visited=new Set()] - Set of already processed vertices.
 * @returns {string|null} The nearest unvisited vertex key.
 */
function minDistanceNode(distances = {}, visited = new Set()) {
    let shortestVertex = null;
    let minDistance = Infinity;

    for (const vertex of Object.keys(distances)) {
        const distance = distances[vertex];
        if (!visited.has(vertex) && distance < minDistance) {
            minDistance = distance;
            shortestVertex = vertex;
        }
    }
    return shortestVertex;
}

/**
 * Relaxes edge distances for all adjacent neighbors of a vertex.
 *
 * @param {Record<string, number>} [neighbors={}] - Adjacent vertices with edge weights.
 * @param {number} [currentDistance=0] - Accumulated distance to current vertex.
 * @param {Record<string, number>} [distances={}] - Global distances table.
 */
function relaxNeighbors(neighbors = {}, currentDistance = 0, distances = {}) {
    for (const neighbor of Object.keys(neighbors)) {
        const newDistance = currentDistance + neighbors[neighbor];
        if (newDistance < distances[neighbor]) {
            distances[neighbor] = newDistance;
        }
    }
}

/**
 * Computes shortest-path distances from a start vertex using Dijkstra's algorithm.
 *
 * @param {Record<string, Record<string, number>>} [graph={}] - Adjacency graph representation.
 * @param {string} [startNode=''] - Source vertex key.
 * @returns {Record<string, number>} Shortest path distances from source.
 */
function dijkstra(graph = {}, startNode = '') {
    const distances = initDistances(graph, startNode);
    const visited = new Set();

    let currentNode = minDistanceNode(distances, visited);
    while (currentNode !== null) {
        const currentDistance = distances[currentNode];
        relaxNeighbors(graph[currentNode], currentDistance, distances);
        visited.add(currentNode);
        currentNode = minDistanceNode(distances, visited);
    }

    return distances;
}

module.exports = { initDistances, minDistanceNode, relaxNeighbors, dijkstra };
