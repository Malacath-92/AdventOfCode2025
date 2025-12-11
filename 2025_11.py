import aocd

import cli

from functools import lru_cache

sample_data = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
data = sample_data if cli.sample else aocd.data


class Device:
    def __init__(self, diagram):
        id, outputs = diagram.split(":")
        self.id = id.strip()
        self.outputs = [o.strip() for o in outputs.strip().split()]


devices = list(map(Device, data.splitlines()))
graph = {d.id: d for d in devices}

root = "you"
target = "out"


def filter_graph(graph):
    stack = []

    inverse_graph = {}
    for id, outputs in graph.items():
        for out in outputs.outputs:
            if out not in inverse_graph:
                inverse_graph[out] = []
            inverse_graph[out].append(id)

    stack.append(target)
    inverse_visited = set()
    while stack:
        current = stack.pop()
        if current in inverse_visited:
            continue
        inverse_visited.add(current)

        for predecessor in inverse_graph.get(current, []):
            if predecessor not in inverse_visited:
                stack.append(predecessor)

    stack.append(root)
    forward_visited = set()
    while stack:
        current = stack.pop()
        if current in forward_visited or current not in graph:
            continue
        forward_visited.add(current)

        for output in graph[current].outputs:
            if output not in forward_visited:
                stack.append(output)

    visited = forward_visited.union(inverse_visited)

    filtered_graph = {}
    for id in visited:
        if id in graph:
            if id not in filtered_graph:
                filtered_graph[id] = Device(id + ":")
            filtered_graph[id].outputs = list(
                filter(lambda x: x in visited, graph[id].outputs)
            )

    return filtered_graph


def get_num_paths(graph, from_node, to_node):
    @lru_cache
    def get_num_paths_impl(current_node):
        if current_node == to_node:
            return 1
        if current_node not in graph:
            return 0

        children = graph[current_node].outputs
        return sum(map(get_num_paths_impl, children))

    return get_num_paths_impl(from_node)


filtered_graph = filter_graph(graph)
num_paths = get_num_paths(filtered_graph, root, target)

print(f"Part 1: {num_paths}")
