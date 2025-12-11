import aocd

import cli

from functools import lru_cache, reduce, partial

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


def filter_graph(graph, root, target):
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


root = "you"
target = "out"
filtered_graph = filter_graph(graph, root, target)

num_paths = get_num_paths(filtered_graph, root, target)
print(f"Part 1: {num_paths}")


if cli.sample:
    data = """\
    svr: aaa bbb
    aaa: fft
    fft: ccc
    bbb: tty
    tty: ccc
    ccc: ddd eee
    ddd: hub
    hub: fff
    eee: dac
    dac: fff
    fff: ggg hhh
    ggg: out
    hhh: out"""
    data = sample_data if cli.sample else aocd.data

    devices = list(map(Device, data.splitlines()))
    graph = {d.id: d for d in devices}


root = "svr"
target = "out"
needs_visit = set(["dac", "fft"])
filtered_graph = filter_graph(graph, root, target)


class SubGraph:
    def __init__(self, graph, sub_root, sub_target):
        self.root = sub_root
        self.target = sub_target
        self.graph = filter_graph(filtered_graph, sub_root, sub_target)

    @property
    def num_paths(self):
        return get_num_paths(self.graph, self.root, self.target)


sub_graphs = []
for interim_node in needs_visit:
    sub_graphs.append(SubGraph(filter_graph, root, interim_node))
    sub_graphs.append(SubGraph(filter_graph, interim_node, target))

    for other_interim_node in needs_visit:
        if interim_node != other_interim_node:
            sub_graphs.append(SubGraph(filter_graph, interim_node, other_interim_node))
sub_graphs = list(filter(lambda g: g.num_paths, sub_graphs))

# Note: We end up having no paths from 'dac' -> 'fft' and thus we can filter out
#       the sub-graph from 'svr' -> 'dac' and 'fft' -> 'out'
#       We determine this programmatically below
for interim_node in needs_visit:
    for other_interim_node in needs_visit:
        if interim_node == other_interim_node:
            continue

        def matching_subgraph(sub_graph, from_node, to_node):
            return sub_graph.root == from_node and sub_graph.target == to_node

        interim_connection = partial(
            matching_subgraph, from_node=interim_node, to_node=other_interim_node
        )
        if not list(filter(interim_connection, sub_graphs)):
            sub_graphs = [
                g
                for g in sub_graphs
                if not matching_subgraph(g, root, interim_node)
                and not matching_subgraph(g, other_interim_node, target)
            ]

sub_graph_num_paths = list(map(lambda g: g.num_paths, sub_graphs))
num_paths = reduce(lambda a, b: a * b, sub_graph_num_paths)
print(f"Part 2: {num_paths}")
