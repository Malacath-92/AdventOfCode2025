import aocd

import cli

from collections import deque

sample_data = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
data = sample_data if cli.sample else aocd.data
total_connections = 10 if cli.sample else 1000


class LightIndicators:
    def __init__(self, lights_diagram):
        assert lights_diagram[-1] == "]"
        self.lights = [l == "#" for l in lights_diagram[1:-1]]


class Button:
    def __init__(self, lights):
        assert lights[-1] == ")"
        self.controlled_lights = list(map(int, lights[1:-1].split(",")))


class JoltageRequirements:
    def __init__(self, req_list):
        assert req_list[-1] == "}"
        self.requirements = list(map(int, req_list[1:-1].split(",")))


class Machine:
    def __init__(self, diagram):
        diagram_parts = diagram.split()
        button_diagrams = diagram_parts[1:-1]

        self.light_indicators = LightIndicators(diagram_parts[0])
        self.buttons = list(map(Button, button_diagrams))
        self.joltage_requirements = JoltageRequirements(diagram_parts[-1])

    @property
    def num_lights(self):
        return len(self.light_indicators.lights)


machines = list(map(Machine, data.splitlines()))


class Lights:
    def __init__(self, lights):
        self.lights = lights[:]

    def push_button(self, button: Button):
        new_state = Lights(self.lights)
        for i in button.controlled_lights:
            new_state.lights[i] = not new_state.lights[i]
        return new_state

    def matches_indicators(self, indicators: LightIndicators):
        return self.lights == indicators.lights


def get_shortest_configure(machine: Machine):
    queue = deque()
    queue.append((Lights([False] * machine.num_lights), 0))

    visited = set()

    # Do a breadth-first-search with cached sub-trees to find the shortest path
    while queue:
        (lights, depth) = queue.popleft()
        for button in machine.buttons:
            # Press button and return immediately if we match the indicators
            switched_lights = lights.push_button(button)
            if switched_lights.matches_indicators(machine.light_indicators):
                return depth + 1

            # Remember this node, getting here later is never worth going deeper
            visited_node = (
                tuple(switched_lights.lights),
                tuple(button.controlled_lights),
            )
            if visited_node in visited:
                continue
            visited.add(visited_node)

            # Queue the new lights, they will handled once we finish this depth
            queue.append((switched_lights, depth + 1))


shortest_configures = list(map(get_shortest_configure, machines))
print(f"Part 1: {sum(shortest_configures)}")
