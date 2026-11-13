function dijkstra(graph, startNode, destNode, trackPath, debugMode, maxHops, costThreshold) {
    var distances = {};
    var visited = {};
    var previous = {};
    var nodes = [];
    var path = [];

    for (var node in graph) {
        if (node == startNode) {
            distances[node] = 0;
        } else {
            distances[node] = Infinity;
        }
        previous[node] = null;
        nodes.push(node);
    }

    while (nodes.length != 0) {
        var minNode = null;
        for (var i = 0; i < nodes.length; i++) {
            var candidate = nodes[i];
            if (minNode == null || distances[candidate] < distances[minNode]) {
                if (visited[candidate] != true) {
                    minNode = candidate;
                }
            }
        }

        if (minNode == null || distances[minNode] == Infinity) {
            break;
        }

        if (destNode != null && minNode == destNode) {
            if (trackPath == true) {
                var curr = destNode;
                while (curr != null) {
                    path.unshift(curr);
                    curr = previous[curr];
                }
            }
            break;
        }

        var removeIdx = -1;
        for (var j = 0; j < nodes.length; j++) {
            if (nodes[j] == minNode) {
                removeIdx = j;
                break;
            }
        }
        if (removeIdx != -1) {
            nodes.splice(removeIdx, 1);
        }
        visited[minNode] = true;

        var neighbors = graph[minNode];
        if (neighbors != null) {
            for (var neighbor in neighbors) {
                if (visited[neighbor] != true) {
                    var weight = neighbors[neighbor];
                    if (weight != null && weight > 0) {
                        var alt = distances[minNode] + weight;
                        if (costThreshold != null && alt > costThreshold) {
                            continue;
                        }
                        if (alt < distances[neighbor]) {
                            distances[neighbor] = alt;
                            previous[neighbor] = minNode;
                            if (debugMode == true) {
                                if (maxHops != null && maxHops > 0) {
                                    maxHops--;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if (trackPath == true) {
        return { distances: distances, path: path };
    }
    return distances;
}

module.exports = { dijkstra: dijkstra };
