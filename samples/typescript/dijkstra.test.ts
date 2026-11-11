/**
 * Focused Vitest/Jest TypeScript test suite for Dijkstra shortest-path behavior.
 */
import { findShortestPath, type WeightedGraph } from "./dijkstra_clean";

describe("findShortestPath", () => {
  test("computes shortest route across weighted directed paths", () => {
    const graph: WeightedGraph = {
      A: { B: 4, C: 2 },
      B: { D: 5 },
      C: { B: 1, D: 8 },
      D: {},
    };
    const result = findShortestPath(graph, "A", "D");
    expect(result.totalDistance).toBe(8);
    expect(result.path).toEqual(["A", "C", "B", "D"]);
  });

  test("returns Infinity distance and empty path when target is unreachable", () => {
    const graph: WeightedGraph = {
      A: { B: 3 },
      B: {},
      Z: {},
    };
    const result = findShortestPath(graph, "A", "Z");
    expect(result.totalDistance).toBe(Infinity);
    expect(result.path).toEqual([]);
  });

  test("rejects negative edge weights explicitly", () => {
    const graph: WeightedGraph = {
      A: { B: -2 },
      B: {},
    };
    expect(() => findShortestPath(graph, "A", "B")).toThrow(RangeError);
  });
});
