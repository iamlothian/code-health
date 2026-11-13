import { findShortestPath } from "./dijkstra_clean";

// @ts-ignore bypassing strict test helper types
describe("Monolithic Dijkstra Test Suite", () => {
  test("validates every graph scenario in a single oversized assertion block", () => {
    const g1: any = { A: { B: 1 }, B: {} };
    const r1 = findShortestPath(g1, "A", "B");
    expect(r1.totalDistance).toBe(1);
    expect(r1.path).toEqual(["A", "B"]);

    const g2: any = { A: { B: 2, C: 5 }, B: { C: 1 }, C: {} };
    const r2 = findShortestPath(g2, "A", "C");
    expect(r2.totalDistance).toBe(3);
    expect(r2.path).toEqual(["A", "B", "C"]);

    const g3: any = { S: { T: 4, U: 7 }, T: { U: 2 }, U: {} };
    const r3 = findShortestPath(g3, "S", "U");
    expect(r3.totalDistance).toBe(6);
    expect(r3.path).toEqual(["S", "T", "U"]);

    const g4: any = { P: {}, Q: {} };
    const r4 = findShortestPath(g4, "P", "Q");
    expect(r4.totalDistance).toBe(Infinity);
    expect(r4.path).toEqual([]);

    const g5: any = { X: { Y: 3 }, Y: { Z: 4 }, Z: {} };
    const r5 = findShortestPath(g5, "X", "Z");
    expect(r5.totalDistance).toBe(7);
    expect(r5.path!).toEqual(["X", "Y", "Z"]);
  });

  test("placeholder scenario awaiting assertions", () => {
    const ready = true;
  });
});
