##############################################
#
# David Parker
# crazdave@gmail.com
#
# 2017
#
##############################################
from graphics import Graphics
import copy
import agents


class GameBoard(object):
    def __init__(self, goal_value, agent=None, graphics=True):
        self.goal = goal_value
        self.graphics = graphics
        self.score = 2
        self._legal_moves = []
        # Initialize state space representation
        self._current_state = {(0, 0): 0, (1, 0): 0, (2, 0): 0, (3, 0): 0,
                               (0, 1): 0, (1, 1): 0, (2, 1): 0, (3, 1): 0,
                               (0, 2): 0, (1, 2): 0, (2, 2): 0, (3, 2): 0,
                               (0, 3): 0, (1, 3): 0, (2, 3): 0, (3, 3): 0}
        # Initialize Graphics and keybindings
        if self.graphics:
            self._root = Graphics()
        self.__random_cell()  # Make first random cell
        self.print_state()
        if not agent:
            self._root.back_grid.bind('<KeyPress-Up>', self.__up)
            self._root.back_grid.bind('<KeyPress-Down>', self.__down)
            self._root.back_grid.bind('<KeyPress-Left>', self.__left)
            self._root.back_grid.bind('<KeyPress-Right>', self.__right)
        # If using AI, initiate first event
        if agent:
            self.agent = agent
            if self.graphics:
                self._root.back_grid.bind('<<Action>>', self._agent_move)  # Bind virtual events
                self._root.back_grid.bind('<<Up>>', self.__up)
                self._root.back_grid.bind('<<Down>>', self.__down)
                self._root.back_grid.bind('<<Left>>', self.__left)
                self._root.back_grid.bind('<<Right>>', self.__right)
                self._root.back_grid.after(100, self._agent_move)  # Start agent move loop
            else:
                self.end = False
                while not self.end:
                    self._agent_move(None)
        # Begin main loop of Tkinter, wait for input
        if self.graphics:
            self._root.mainloop()

    def get_current_state(self):
        return copy.deepcopy(self._current_state)

    def get_actions(self, state=None):
        up, down, left, right = False, False, False, False
        if not state:
            state = self._current_state
        if self.is_goal_state(state):
            return []
        else:
            move_list = []
            for y in range(4):
                for x in range(4):
                    if state[x, y] != 0:
                        # Look at up possibility
                        if not up and y > 0:
                            up = state[x, y] == state[x, y-1] or state[x, y-1] == 0
                            if up:
                                move_list.append('Up')
                        # Down possibility
                        if not down and y < 3:
                            down = state[x, y] == state[x, y+1] or state[x, y+1] == 0
                            if down:
                                move_list.append('Down')
                        # Left possibility
                        if not left and x > 0:
                            left = state[x, y] == state[x-1, y] or state[x-1, y] == 0
                            if left:
                                move_list.append('Left')
                        # Right possibility
                        if not right and x < 3:
                            right = state[x, y] == state[x+1, y] or state[x+1, y] == 0
                            if right:
                                move_list.append('Right')
            return move_list


    def get_next_state(self, state, action):  # Returns the state after action but before a random cell has been placed
        temp_state = copy.deepcopy(self._current_state)  # COPY current state
        self._current_state = copy.deepcopy(state)  # Change current state to match argument
        if action == 'Up':
            self.__up(None, False)
        elif action == 'Down':
            self.__down(None, False)
        elif action == 'Left':
            self.__left(None, False)
        elif action == 'Right':
            self.__right(None, False)
        # self._root.back_grid.event_generate('<<Fake'+action+'>>')  # Perform action w/o graphics
        out_state = self._current_state  # Save changed state
        self._current_state = temp_state  # Replace previous state as current again
        return out_state  # Output the changed state

    def get_possible_states(self, state):  # Returns a list of possible states by filling each empty slot
        temp_state = copy.deepcopy(state)  # Copy state
        out_list = []  # List to output
        for coord, val in temp_state.iteritems():
            if not val:  # For each cell that's 0
                temp_state[coord] = 2  # Change val to 2
                out_list.append(copy.deepcopy(temp_state))  # Append a copy
                temp_state[coord] = 0
        return out_list

    def is_goal_state(self, state):  # Returns whether the passed state is the goal
        for coord in state:
            if state[coord] >= self.goal:
                return True
        return False

    def is_lose_state(self, state):
        if not self.get_actions(state):
            return True
        else:
            return False

    def _agent_move(self, event=None):
        if self.is_goal_state(self._current_state):
            print "Win!"
            self.end = True
            self.print_state()
            return
        if self.is_lose_state(self._current_state):
            print "Lose :("
            self.end = True
            self.print_state()
            return
        action = self.agent.get_action(self)
        if self.graphics:
            self._root.back_grid.after(0, self._root.back_grid.event_generate, '<<'+action+'>>')
            self._root.back_grid.after(400, self._root.back_grid.event_generate, '<<Action>>')  # Get another action
        else:
            if action == 'Up':
                self.__up(None)
            elif action == 'Down':
                self.__down(None)
            elif action == 'Left':
                self.__left(None)
            elif action == 'Right':
                self.__right(None)

    def print_state(self, state=None):
        if not state:
            state = self._current_state
        for y in range(0, 4):
            for x in range(0, 4):
                print state[x, y],
            print ''

    def __up(self, event, real=True):
        if real:
            if 'Up' not in self._legal_moves:
                return
            print 'Move up'
        # Setup loop to scan in correct order, top to bottom
        for y in range(1, 4):
            for x in range(0, 4):
                if self._current_state[x, y]:
                    collide, new_y = self.__collision((x, y), 'Up')
                    if collide:
                        self._current_state[x, new_y] *= 2
                        if real:
                            self.score += self._current_state[x, new_y]
                        self._current_state[x, y] = 0
                    elif y != new_y:
                        self._current_state[x, new_y] = self._current_state[x, y]
                        self._current_state[x, y] = 0
                    if real and self.graphics:
                        self._root.up(x, y, x, new_y, collide, self._current_state[x, new_y])
        if real:
            self.__random_cell()
            if self.graphics:
                self.print_state()

    def __down(self, event, real=True):
        if real:
            if 'Down' not in self._legal_moves:
                return
            print 'Move down'
        # Setup loop to scan in correct order, bottom to top
        for y in reversed(range(0, 3)):
            for x in range(0, 4):
                if self._current_state[x, y]:
                    collide, new_y = self.__collision((x, y), 'Down')
                    if collide:
                        self._current_state[x, new_y] *= 2
                        if real:
                            self.score += self._current_state[x, new_y]
                        self._current_state[x, y] = 0
                    elif y != new_y:
                        self._current_state[x, new_y] = self._current_state[x, y]
                        self._current_state[x, y] = 0
                    if real and self.graphics:
                        self._root.down(x, y, x, new_y, collide, self._current_state[x, new_y])
        if real:
            self.__random_cell()
            if self.graphics:
                self.print_state()

    def __left(self, event, real=True):
        if real:
            if 'Left' not in self._legal_moves:
                return
            print 'Move left'
        # Setup loop to scan in correct order, left to right
        for x in range(1, 4):
            for y in range(0, 4):
                if self._current_state[x, y]:
                    collide, new_x = self.__collision((x, y), 'Left')
                    if collide:
                        self._current_state[new_x, y] *= 2
                        if real:
                            self.score += self._current_state[new_x, y]
                        self._current_state[x, y] = 0
                    elif x != new_x:
                        self._current_state[new_x, y] = self._current_state[x, y]
                        self._current_state[x, y] = 0
                    if real and self.graphics:
                        self._root.left(x, y, new_x, y, collide, self._current_state[new_x, y])
        if real:
            self.__random_cell()
            if self.graphics:
                self.print_state()

    def __right(self, event, real=True):
        if real:
            if 'Right' not in self._legal_moves:
                print self._legal_moves
                return
            print 'Move right'
        # Setup loop to scan in correct order, right to left
        for x in reversed(range(0, 3)):
            for y in range(0, 4):
                if self._current_state[x, y]:
                    collide, new_x = self.__collision((x, y), 'Right')
                    if collide:
                        self._current_state[new_x, y] *= 2
                        if real:
                            self.score += self._current_state[new_x, y]
                        self._current_state[x, y] = 0
                    elif x != new_x:
                        self._current_state[new_x, y] = self._current_state[x, y]
                        self._current_state[x, y] = 0
                    if real and self.graphics:
                        self._root.right(x, y, new_x, y, collide, self._current_state[new_x, y])
        if real:
            self.__random_cell()
            if self.graphics:
                self.print_state()

    def __collision(self, (x, y), move):
        if move == 'Up':
            for i in reversed(range(0, y)):
                if self._current_state[x, i] == self._current_state[x, y]:
                    return True, i
                elif self._current_state[x, i]:
                    return False, i + 1
            return False, 0
        elif move == 'Down':
            for i in range(y + 1, 4):
                if self._current_state[x, i] == self._current_state[x, y]:
                    return True, i
                elif self._current_state[x, i]:
                    return False, i - 1
            return False, 3
        elif move == 'Left':
            for i in reversed(range(0, x)):
                if self._current_state[i, y] == self._current_state[x, y]:
                    return True, i
                elif self._current_state[i, y]:
                    return False, i + 1
            return False, 0
        elif move == 'Right':
            for i in range(x + 1, 4):
                if self._current_state[i, y] == self._current_state[x, y]:
                    return True, i
                elif self._current_state[i, y]:
                    return False, i - 1
            return False, 3

    def __random_cell(self):
        from random import randint
        # Keep getting random numbers until we have a blank cell
        index = randint(0, 15)
        x_rand = index % 4
        y_rand = index / 4
        while self._current_state[x_rand, y_rand] != 0:
            x_rand = randint(0, 3)
            y_rand = randint(0, 3)
        # Call graphics to display a new cell
        if self.graphics:
            self._root.new_cell(x_rand, y_rand)
        self._current_state[x_rand, y_rand] = 2
        self._legal_moves = self.get_actions(self._current_state)
        print 'Score:', self.score


if __name__ == "__main__":
    # To adjust weights ##############
    # import random
    # weight_1 = agents.weight_1 + 0.0
    # weight_2 = agents.weight_2 + 0.0
    # weight_3 = agents.weight_3 + 0.0
    # weight_4 = agents.weight_4 + 0.0
    # weight_5 = agents.weight_5 + 0.0
    # with open('results_final.txt', 'a') as f:
    #     for i in range(1):
    #         myAgent = agents.ExpectimaxAgent(depth=1)
    #         f.write('---- AGENT ' + str(i) + '\n')
    #         f.write('WEIGHTS\n')
    #         f.write('1: ' + str(agents.weight_1) + '\n')
    #         f.write('2: ' + str(agents.weight_2) + '\n')
    #         f.write('3: ' + str(agents.weight_3) + '\n')
    #         f.write('4: ' + str(agents.weight_4) + '\n')
    #         f.write('5: ' + str(agents.weight_5) + '\n')
    #         wins = []
    #         f.write('RESULTS\n')
    #         for j in range(30):
    #             if j == 0:
    #                 game = GameBoard(goal, myAgent, graphics=True)
    #             else:
    #                 game = GameBoard(goal, myAgent, graphics=False)
    #             f.write('---- GAME ' + str(j) + '\n')
    #             state = game.get_current_state()
    #             if game.is_goal_state(state):
    #                 wins.append(game.score)
    #                 f.write('Win: ' + str(game.score) + '\n')
    #             else:
    #                 f.write('Lose: ' + str(game.score) + '\n')
    #             f.write('Largest: ' + str(state[max(state, key=state.get)]) + '\n')
    #         if wins:
    #             f.write('Won ' + str(len(wins)) + '/30 Avg:' + str(sum(wins)/len(wins)) + '\n')
    #         #agents.weight_1 = weight_1 + float(random.randint(-5, 5)) / float(random.randint(1, 10))
    #         #agents.weight_2 = weight_2 + float(random.randint(-4, 4)) / float(random.randint(1, 10))
    #         #agents.weight_3 = weight_3 + float(random.randint(-3, 3)) / float(random.randint(1, 10))
    #         agents.weight_4 = weight_4 + float(random.randint(-5, 5)) / float(random.randint(1, 10))
    #         agents.weight_5 = weight_5 + float(random.randint(-5, 5)) / float(random.randint(1, 10))
    import argparse
    parser = argparse.ArgumentParser(description='2048 Game w/ AI')
    parser.add_argument('-a', '--agent', type=str, help='name of agent (Reflex or Expectimax)')
    parser.add_argument('-d', '--depth', type=int, default=2, help='depth for Expectimax (Default: 2)')
    parser.add_argument('-g', '--goal', type=int, default=2048, help='number of goal for AI (Default: 2048)')
    parser.add_argument('--no-graphics', action='store_true', help='no graphics (only works when AI specified)')
    args = parser.parse_args()

    myAgent = None
    graphics = True
    if args.agent == 'Reflex':
        myAgent = agents.ReflexAgent()
    elif args.agent == 'Expectimax':
        myAgent = agents.ExpectimaxAgent(depth=args.depth)
    if args.no_graphics and args.agent:
        graphics = False

    game = GameBoard(args.goal, myAgent, graphics)
