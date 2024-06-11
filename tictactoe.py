import random


class TicTacToe:
    def __init__(self, h=3, w=3, k=3):
        self.h = h
        self.w = w
        self.k = k
        steps = [(x, y) for x in range(1, h + 1) for y in range(1, w + 1)]
        self.initial = {'next': 'X', 'result': 0, 'board': {}, 'steps': steps}

    def next(self, state):
        """Return who is the next player"""
        return state['next']

    def legal_steps(self, state):
        """We can steps on every empty cell"""
        return state['steps']

    def take_step(self, step, state):
        """Effect of the step to the State game representation"""
        if step not in self.legal_steps(state):
            return state

        board = state['board'].copy()
        board[step] = state['next']
        steps = list(state['steps'])
        steps.remove(step)
        return {
            'next': 'X' if state['next'] == 'O' else 'O',
            'result': self.result(board, step, state['next']),
            'board': board,
            'steps': steps
        }

    def next_state(self, state):
        """Return next (step, state) list."""
        return [(step, self.take_step(step, state)) for step in self.legal_steps(state)]

    def result(self, board, step, player):
        """If X wins with this Step the return 1. If O wins with this Step then return -1.
        Else return 0"""
        if (self.check_triples(board, step, player, (0, 1)) or self.check_triples(board, step, player, (1, 0)) or
                self.check_triples(board, step, player, (1, -1)) or self.check_triples(board, step, player, (1, 1))):
            return 1 if player == 'X' else -1

        return 0

    def check_triples(self, board, step, player, direction):
        """Check for triples in a given direction"""
        delta_x, delta_y = direction
        x, y = step
        n = 0
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = step
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # avoid double-counting the original position
        return n >= self.k

    def goodness(self, state, player):
        """X goodness: 1 if it wins, -1 if it loses, 0 if it draws."""
        return state['result'] if player == "X" else -state['result']

    def is_leaf(self, state):
        """If someone won or the table is full, it will be the end of the game."""
        return state['result'] != 0 or len(state['steps']) == 0

    def print(self, state):
        board = state['board']
        for x in range(1, self.h + 1):
            for y in range(1, self.w + 1):
                print(board.get((x, y), '.'), end=" ")
            print()
        print("Result of the game: ", state['result'])
        print()


def state_to_str(state):
    """Encode the given state into a string-state in 3 by 3 board"""
    result = [[" ", " ", " "] for r in range(3)]
    for k, v in state["board"].items():
        result[k[0] - 1][k[1] - 1] = v

    return "\n".join(["|".join(r) for r in result])


# Players
def random_player(game, state):
    return random.choice(game.legal_steps(state))


def play_game(game, *players):
    state = game.initial
    game.print(state)

    while True:
        for player in players:
            step = player(game, state)
            state = game.take_step(step, state)
            game.print(state)
            if game.is_leaf(state):
                end_result = game.goodness(state, 'X')
                return "X wins" if end_result == 1 else "O wins" if end_result == -1 else "Draw"


def main():
    tic_tac_toe = TicTacToe()
    print(tic_tac_toe.initial)
    print("Random player VS Random player: ", play_game(tic_tac_toe, random_player, random_player))


if __name__ == '__main__':
    main()
