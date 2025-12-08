import aocd

import cli

from vector import Vector as Vector

from itertools import combinations
from functools import reduce
from collections import defaultdict

sample_data = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
data = sample_data if cli.sample else aocd.data
total_connections = 10 if cli.sample else 1000

boxes = [Vector(*map(int, line.split(","))) for line in data.splitlines()]

connections = list(combinations(boxes, r=2))
connections_with_distances = [
    ((lhs - rhs).len_sqr, (lhs, rhs)) for lhs, rhs in connections
]
connections_with_distances_sorted = sorted(
    connections_with_distances, key=lambda x: x[0]
)
connections_sorted = list(map(lambda x: x[1], connections_with_distances_sorted))

circuits = {}
for lhs, rhs in connections_sorted[:total_connections]:
    if lhs not in circuits:
        circuits[lhs] = len(circuits)
    lhs_circuit = circuits[lhs]

    if rhs not in circuits:
        circuits[rhs] = lhs_circuit
        continue
    rhs_circuit = circuits[rhs]

    if lhs_circuit != rhs_circuit:
        for box, circuit_id in circuits.items():
            if circuit_id == rhs_circuit:
                circuits[box] = lhs_circuit

circuit_sizes = defaultdict(lambda: 0)
for circuit_id in circuits.values():
    circuit_sizes[circuit_id] += 1
circuit_sizes = list(circuit_sizes.values())
biggest_circuits = sorted(circuit_sizes, reverse=True)[:3]

print("Part 1:", reduce(lambda a, b: a * b, biggest_circuits))

def find_last_connection():
    circuits = {
        box: circuit_id for circuit_id, box in enumerate(boxes)
    }
    for lhs, rhs in connections_sorted:
        lhs_circuit = circuits[lhs]
        rhs_circuit = circuits[rhs]
        if lhs_circuit != rhs_circuit:
            for box, circuit_id in circuits.items():
                if circuit_id == rhs_circuit:
                    circuits[box] = lhs_circuit
            if len(set(circuits.values())) == 1:
                return (lhs, rhs)
    return None

last_connection = find_last_connection()
print(f"Part 2: {last_connection[0].x * last_connection[1].x}")
