const { dijkstra } = require('./dijkstra_clean');

describe('Dijkstra Shortest Path Algorithm', () => {
    test('computes shortest path on linear chain graph', () => {
        const graph = {
            A: { B: 2 },
            B: { C: 3 },
            C: {}
        };
        const distances = dijkstra(graph, 'A');
        expect(distances.A).toEqual(0);
        expect(distances.B).toEqual(2);
        expect(distances.C).toEqual(5);
    });

    test('computes shortest path choosing cheaper branch', () => {
        const graph = {
            A: { B: 10, C: 3 },
            C: { B: 2 },
            B: {}
        };
        const distances = dijkstra(graph, 'A');
        expect(distances.B).toEqual(5);
        expect(distances.C).toEqual(3);
    });

    test('assigns Infinity for disconnected vertices', () => {
        const graph = {
            A: { B: 1 },
            B: {},
            Z: {}
        };
        const distances = dijkstra(graph, 'A');
        expect(distances.Z).toEqual(Infinity);
    });
});
