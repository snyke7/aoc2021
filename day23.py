from typing import Tuple, Optional, List
import attr


HALLWAY_PASS = {
    0: {
        0: ({1}, 3),
        1: ({1, 2}, 5),
        2: ({1, 2, 3}, 7),
        3: ({1, 2, 3, 4}, 9),
    },
    1: {
        0: (set(), 2),
        1: ({2}, 4),
        2: ({2, 3}, 6),
        3: ({2, 3, 4}, 8)
    },
    2: {
        0: (set(), 2),
        1: (set(), 2),
        2: ({3}, 4),
        3: ({3, 4}, 6)
    },
    3: {
        0: ({2}, 4),
        1: (set(), 2),
        2: (set(), 2),
        3: ({4}, 4)
    },
    4: {
        0: ({2, 3}, 6),
        1: ({3}, 4),
        2: (set(), 2),
        3: (set(), 2)
    },
    5: {
        0: ({2, 3, 4}, 8),
        1: ({3, 4}, 6),
        2: ({4}, 4),
        3: (set(), 2)
    },
    6: {
        0: ({2, 3, 4, 5}, 9),
        1: ({3, 4, 5}, 7),
        2: ({4, 5}, 5),
        3: ({5}, 3)
    },
}


@attr.s(auto_attribs=True, frozen=True)
class AmphipodFloor:
    sockets: Tuple[Tuple[int]]
    hallways: Tuple[int] = (0,) * 7

    def get_sinkable_hallway(self) -> Optional[int]:
        for i, el in enumerate(self.hallways):
            if el != 0:
                socket = el - 1
                if all((self.hallways[to_pass] == 0 for to_pass in HALLWAY_PASS[i][socket][0])):
                    # amphipod can move to socket entry
                    if self.get_first_available_socket(socket) is not None:
                        # amphipod is allowed to enter socket
                        return i
        return None

    def get_first_available_socket(self, socket):
        if not self.can_sink_in(socket):
            return None
        for idx, el in enumerate(reversed(self.sockets[socket])):
            if el == 0:
                return len(self.sockets[socket]) - 1 - idx
        return None

    def can_sink_in(self, socket):
        return all((el == 0 or el == socket + 1 for el in self.sockets[socket]))

    def get_first_movable_amphipod(self, socket):
        if self.can_sink_in(socket):
            return None
        for idx, el in enumerate(self.sockets[socket]):
            if el != 0:
                return idx
        return None

    def is_done(self):
        return all((self.can_sink_in(socket) for socket in range(4))) and all((el == 0 for el in self.hallways))

    def get_possible_moves(self):
        # if any amphipod can be sinked, wlog: only show that move as possible
        hallway_sink = self.get_sinkable_hallway()
        if hallway_sink is not None:
            socket = self.hallways[hallway_sink] - 1
            cost = HALLWAY_PASS[hallway_sink][socket][1]
            available_socket = self.get_first_available_socket(socket)
            cost += available_socket
            cost *= 10 ** socket
            new_socket_list: List[List[int]] = list(map(list, self.sockets))
            new_socket_list[socket][available_socket] = self.hallways[hallway_sink]
            new_hallway_list = list(self.hallways)
            new_hallway_list[hallway_sink] = 0
            return [(AmphipodFloor(tuple(map(tuple, new_socket_list)), tuple(new_hallway_list)), cost)]
        # otherwise: move amphipod from unmatching socket to available hallway
        result = []
        for socket in range(4):
            movable = self.get_first_movable_amphipod(socket)
            if movable is None:
                continue
            for hallway in range(7):
                if all((self.hallways[to_pass] == 0 for to_pass in HALLWAY_PASS[hallway][socket][0])) and self.hallways[hallway] == 0:
                    cost = HALLWAY_PASS[hallway][socket][1]
                    cost += movable
                    cost *= 10 ** (self.sockets[socket][movable] - 1)
                    new_hallway_list = list(self.hallways)
                    new_hallway_list[hallway] = self.sockets[socket][movable]
                    new_socket_list: List[List[int]] = list(map(list, self.sockets))
                    new_socket_list[socket][movable] = 0
                    result.append((AmphipodFloor(tuple(map(tuple, new_socket_list)), tuple(new_hallway_list)), cost))
        return result


def dijkstra_floor(start_floor):
    lowest_cost_map = {start_floor: 0}
    new_floors = {start_floor}
    min_done = float('inf')
    done_state = None
    while new_floors:
        new_floor = new_floors.pop()
        cur_cost = lowest_cost_map[new_floor]
        if new_floor.is_done():
            min_done = min(min_done, cur_cost)
            done_state = new_floor
            continue
        if cur_cost > min_done:
            continue
        for move, move_cost in new_floor.get_possible_moves():
            if move not in lowest_cost_map or lowest_cost_map[move] > cur_cost + move_cost:
                lowest_cost_map[move] = cur_cost + move_cost
                new_floors.add(move)
    return lowest_cost_map[done_state]


def get_solution():
    test_floor2 = AmphipodFloor(tuple(map(tuple, [
        [2, 1],
        [3, 4],
        [2, 3],
        [4, 1],
    ])))
    real_floor2 = AmphipodFloor(tuple(map(tuple, [
        [4, 3],
        [3, 4],
        [1, 1],
        [2, 2],
    ])))
    test_floor4 = AmphipodFloor(tuple(map(tuple, [
        [2, 4, 4, 1],
        [3, 3, 2, 4],
        [2, 2, 1, 3],
        [4, 1, 3, 1],
    ])))
    real_floor4 = AmphipodFloor(tuple(map(tuple, [
        [4, 4, 4, 3],
        [3, 3, 2, 4],
        [1, 2, 1, 1],
        [2, 1, 3, 2],
    ])))
    print(dijkstra_floor(test_floor2))
    print(dijkstra_floor(real_floor2))
    print(dijkstra_floor(test_floor4))
    print(dijkstra_floor(real_floor4))

