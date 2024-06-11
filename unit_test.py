import unittest
from tictactoe import TicTacToe, state_to_str


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.game = TicTacToe()
        self.initial_state = self.game.initial
        self.state_x_win = {
            'next': 'O',
            'result': 1,
            'board': {(1, 1): 'X', (1, 2): 'X', (1, 3): 'X', (2, 1): 'O', (3, 1): 'O'},
            'steps': [(2, 2), (2, 3), (3, 2), (3, 3)]
        }
        self.state_o_win = {
            'next': 'X',
            'result': -1,
            'board': {(1, 1): 'O', (2, 2): 'O', (3, 3): 'O', (1, 2): 'X', (1, 3): 'X'},
            'steps': [(2, 1), (2, 3), (3, 1), (3, 2)]
        }
        self.state_draw = {
            'next': 'O',
            'result': 0,
            'board': {
                (1, 1): 'X', (1, 2): '0', (1, 3): 'X',
                (2, 1): 'X', (2, 2): '0', (2, 3): '0',
                (3, 1): '0', (3, 2): 'X', (3, 3): 'X'
            },
            'steps': []
        }

    def test_initial_state(self):
        self.assertEqual(self.initial_state['next'], 'X')
        self.assertEqual(self.initial_state['result'], 0)
        self.assertEqual(len(self.initial_state['board']), 0)
        self.assertEqual(len(self.initial_state['steps']), 9)

    def test_legal_steps_initial(self):
        state = self.initial_state
        legal_steps = self.game.legal_steps(state)

        self.assertEqual(len(legal_steps), 9)

    def test_take_step(self):
        state = self.initial_state
        step = (1, 1)
        new_state = self.game.take_step(step, state)

        self.assertEqual(new_state['board'][step], 'X')
        self.assertEqual(new_state['next'], 'O')
        self.assertNotIn(step, new_state['steps'])

    def test_result_x_wins(self):
        state = self.state_x_win
        self.assertEqual(self.game.result(state['board'], (1, 3), 'X'), 1)

    def test_result_o_wins(self):
        state = self.state_o_win
        self.assertEqual(self.game.result(state['board'], (3, 3), 'O'), -1)

    def test_is_leaf(self):
        state_x_win = self.state_x_win
        state_o_win = self.state_o_win
        state_draw = self.state_draw

        self.assertTrue(self.game.is_leaf(state_x_win))
        self.assertTrue(self.game.is_leaf(state_o_win))
        self.assertTrue(self.game.is_leaf(state_draw))

    def test_goodness(self):
        state_x_win = self.state_x_win
        state_x_lose = self.state_o_win
        state_o_win = self.state_o_win
        state_o_lose = self.state_x_win
        state_draw = self.state_draw

        self.assertEqual(self.game.goodness(state_x_win, 'X'), 1)
        self.assertEqual(self.game.goodness(state_x_lose, 'X'), -1)
        self.assertEqual(self.game.goodness(state_o_win, 'O'), 1)
        self.assertEqual(self.game.goodness(state_o_lose, 'O'), -1)
        self.assertEqual(self.game.goodness(state_draw, 'X'), 0)

    def test_state_to_str(self):
        state = self.state_o_win

        state_str = state_to_str(state)
        expected_str = "O|X|X\n |O| \n | |O"
        self.assertEqual(state_str, expected_str)


if __name__ == "__main__":
    unittest.main()


