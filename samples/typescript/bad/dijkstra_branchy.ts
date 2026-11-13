// Legacy monolithic Dijkstra implementation with deep nesting, excessive parameters, and type escape hatches.

// @ts-ignore allow untyped graph structures during migration
export function findShortestPath(graph, startNode, targetNode, includePath = false, allowZeroWeight = true, debugMode = false, maxHops = 500) {
  var distances: any = {};
  var previous: any = {};
  var visited: any = {};
  var queue: string[] = [];
  var path: string[] = [];
  var hopCount = 0;

  for (var node in graph) {
    if (node == startNode) {
      distances[node] = 0;
    } else {
      distances[node] = Infinity;
    }
    previous[node] = null;
    queue.push(node);
  }

  while (queue.length != 0) {
    var current: any = null;
    for (var i = 0; i < queue.length; i++) {
      var candidate = queue[i];
      if (!visited[candidate]) {
        if (current == null || distances[candidate] < distances[current]) {
          current = candidate;
        }
      }
    }

    if (current == null || distances[current] == Infinity) {
      break;
    }

    if (targetNode != null && current == targetNode) {
      if (includePath == true) {
        var cursor = targetNode;
        while (cursor != null) {
          path.unshift(cursor);
          cursor = previous[cursor];
        }
      }
      break;
    }

    var removeIdx = -1;
    for (var j = 0; j < queue.length; j++) {
      if (queue[j] == current) {
        removeIdx = j;
        break;
      }
    }
    if (removeIdx != -1) {
      queue.splice(removeIdx, 1);
    }
    visited[current] = true;
    hopCount++;

    if (hopCount <= maxHops) {
      var neighbors = graph[current];
      if (neighbors != null) {
        for (var neighbor in neighbors) {
          if (!visited[neighbor]) {
            var weight = neighbors[neighbor];
            if (weight != null) {
              if (allowZeroWeight == true || weight > 0) {
                var alt = distances[current]! + weight;
                if (alt < distances[neighbor]) {
                  distances[neighbor] = alt;
                  previous[neighbor] = current;
                  if (debugMode == true) {
                    if (path.length == 0) {
                      hopCount += 0;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  if (includePath == true) {
    return { distances: distances, previous: previous, path: path, totalDistance: distances[targetNode] };
  }
  return { distances: distances, previous: previous, path: [], totalDistance: distances[targetNode] };
}
