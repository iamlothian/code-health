/**
 * Strongly typed Dijkstra shortest-path algorithm with modular relaxation helpers
 * and path reconstruction.
 */

export type WeightedGraph = Readonly<Record<string, Readonly<Record<string, number>>>>;

export interface ShortestPathResult {
  readonly distances: Record<string, number>;
  readonly previous: Record<string, string | null>;
  readonly path: string[];
  readonly totalDistance: number;
}

/** Initialize vertex distance and predecessor tables for Dijkstra traversal. */
export function initializeDistances(
  graph: WeightedGraph,
  startNode: string,
): { distances: Record<string, number>; previous: Record<string, string | null> } {
  const distances: Record<string, number> = {};
  const previous: Record<string, string | null> = {};

  for (const node of Object.keys(graph)) {
    distances[node] = Infinity;
    previous[node] = null;
  }
  if (Object.prototype.hasOwnProperty.call(distances, startNode)) {
    distances[startNode] = 0;
  }
  return { distances, previous };
}

/** Select the unvisited vertex with the lowest accumulated distance. */
export function findNearestUnvisited(
  distances: Readonly<Record<string, number>>,
  visited: ReadonlySet<string>,
): string | null {
  let nearestNode: string | null = null;
  let shortestDistance = Infinity;

  for (const vertex of Object.keys(distances)) {
    const candidate = distances[vertex];
    if (!visited.has(vertex) && candidate < shortestDistance) {
      shortestDistance = candidate;
      nearestNode = vertex;
    }
  }
  return nearestNode;
}

/** Relax outgoing edges from the active vertex when a shorter path is discovered. */
export function relaxNeighborEdges(
  neighbors: Readonly<Record<string, number>>,
  currentNode: string,
  distances: Record<string, number>,
  previous: Record<string, string | null>,
): void {
  const baseDistance = distances[currentNode];
  for (const neighbor of Object.keys(neighbors)) {
    const weight = neighbors[neighbor];
    if (weight < 0) {
      throw new RangeError(`Edge weight from ${currentNode} to ${neighbor} must be non-negative.`);
    }
    const candidateDistance = baseDistance + weight;
    if (candidateDistance < (distances[neighbor] ?? Infinity)) {
      distances[neighbor] = candidateDistance;
      previous[neighbor] = currentNode;
    }
  }
}

/** Reconstruct the ordered path from source to target using predecessor links. */
export function reconstructPath(
  previous: Readonly<Record<string, string | null>>,
  targetNode: string,
): string[] {
  const path: string[] = [];
  let cursor: string | null = targetNode;
  while (cursor !== null) {
    path.unshift(cursor);
    cursor = previous[cursor] ?? null;
  }
  return path;
}

/** Compute shortest paths and optional target path in a non-negative weighted graph. */
export function findShortestPath(
  graph: WeightedGraph,
  startNode: string,
  targetNode: string,
): ShortestPathResult {
  const { distances, previous } = initializeDistances(graph, startNode);
  const visited = new Set<string>();

  let current = findNearestUnvisited(distances, visited);
  while (current !== null) {
    visited.add(current);
    if (current === targetNode) {
      break;
    }
    relaxNeighborEdges(graph[current] ?? {}, current, distances, previous);
    current = findNearestUnvisited(distances, visited);
  }

  const totalDistance = distances[targetNode] ?? Infinity;
  const path = Number.isFinite(totalDistance) ? reconstructPath(previous, targetNode) : [];
  return { distances, previous, path, totalDistance };
}
