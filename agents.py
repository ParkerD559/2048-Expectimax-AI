from math import log


class ReflexAgent(object):
    def __init__(self):
        pass

    def evaluation(self, game, action):
        current_state = game.get_current_state()
        next_state = game.get_next_state(current_state, action)

        adjacent_cells = 0
        next_empty_slots = 0
        for coord in next_state:
            if not next_state[coord]:
                next_empty_slots += 1
            else:
                x, y = coord
                if x > 0 and next_state[coord] == next_state[x-1, y]:
                    adjacent_cells += 1
                if x < 3 and next_state[coord] == next_state[x+1, y]:
                    adjacent_cells += 1
                if y > 0 and next_state[coord] == next_state[x, y-1]:
                    adjacent_cells += 1
                if y < 3 and next_state[coord] == next_state[x, y+1]:
                    adjacent_cells += 1

        max_tile = next_state[max(next_state, key=next_state.get)]

        return next_empty_slots + max_tile + adjacent_cells

    def get_action(self, game):
        evals = []
        for action in game.get_actions():
            evals.append((action, self.evaluation(game, action)))
        return max(evals, key=lambda item: item[1])[0]


class ExpectimaxAgent(object):
    def __init__(self, depth=2):
        self.depth = depth

    def evaluation(self, state):
        weight_1 = 18.992
        weight_2 = 13.959
        weight_3 = 7.05
        weight_4 = 0.967
        weight_5 = -0.682

        max_cell = log(state[max(state, key=state.get)], 2)

        free_tiles = 0.0
        adjacent_sum = 1.0
        adjacent_cells = 0.0
        edges_sum = 0.0
        # diff_adjacent_cells = 0.0
        sum_tiles = 0.0
        for coord in state:
            if not state[coord]:
                free_tiles += 1.0
            else:
                sum_tiles += state[coord]
                x, y = coord
                if x > 0 and state[x-1, y]:
                    adjacent_sum += abs(log(state[coord], 2) - log(state[x-1, y], 2))
                    if state[coord] == state[x-1, y]:
                        adjacent_cells += 1.0
                elif x == 0:
                    edges_sum += log(state[coord], 2)
                if x < 3 and state[x+1, y]:
                    adjacent_sum += abs(log(state[coord], 2) - log(state[x+1, y], 2))
                    if state[coord] == state[x+1, y]:
                        adjacent_cells += 1.0
                elif x == 3:
                    edges_sum += log(state[coord], 2)
                if y > 0 and state[x, y-1]:
                    adjacent_sum += abs(log(state[coord], 2) - log(state[x, y-1], 2))
                    if state[coord] == state[x, y-1]:
                        adjacent_cells += 1.0
                elif y == 0:
                    edges_sum += log(state[coord], 2)
                if y < 3 and state[x, y+1]:
                    adjacent_sum += abs(log(state[coord], 2) - log(state[x, y+1], 2))
                    if state[coord] == state[x, y+1]:
                        adjacent_cells += 1.0
                elif y == 3:
                    edges_sum += log(state[coord], 2)

        return (max_cell * weight_1) + \
               (free_tiles * weight_2) + \
               (adjacent_cells * weight_3) + \
               (edges_sum * weight_4) + \
               (adjacent_sum * weight_5)

    def get_action(self, game):
        move_tuple = self.max_value(game, game.get_current_state())
        print move_tuple[1]
        return move_tuple[0]

    def max_value(self, game, state):
        # Leaf node
        if not game.get_actions(state) or self.depth == 0:
            # game.print_state(state)
            return "", self.evaluation(state)
        # Initialize list of successor nodes
        successor_values = []
        for action in game.get_actions():
            recursive_agent = ExpectimaxAgent(depth=self.depth)
            successor_values.append((action, recursive_agent.chance_value(game, game.get_next_state(state, action))[1]))
        return max(successor_values, key=lambda item: item[1])

    def chance_value(self, game, state):
        # Leaf node
        if not game.get_actions(state) or self.depth == 0:
            return "", self.evaluation(state)
        # Variable for value sum of all possible taken cells
        successor_sum = 0.0
        possible_states = game.get_possible_states(state)
        if possible_states:
            option_weight = 1.0 / len(possible_states)
        else:
            option_weight = 1.0
        for possibility in possible_states:
            recursive_agent = ExpectimaxAgent(depth=self.depth - 1)
            successor_sum += recursive_agent.max_value(game, possibility)[1] * option_weight
        return "", successor_sum
