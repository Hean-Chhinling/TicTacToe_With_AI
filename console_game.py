import pickle
from tictactoe import TicTacToe, state_to_str


def main():
    tic_tac_toe = TicTacToe()
    agent_f = open(
        "tic_tac_toe_agent.pkl", "rb")
    ttt_agent = pickle.load(agent_f)
    state_to_id_f = open(
        "state_to_id.pkl", "rb"
    )
    state_to_id = pickle.load(state_to_id_f)

    state = tic_tac_toe.initial
    state_representation = state_to_str(state)
    if state_representation not in state_to_id:
        state_to_id[state_representation] = len(state_to_id)

    is_done = False

    while not is_done:
        action = ttt_agent.act(state=state_to_id[state_representation], epsilon=0)
        action_tuple = ((action//3) + 1, (action % 3) + 1)

        if action_tuple not in state['steps']:
            print("Game over (Illegal step taken by the agent)")  # It cannot recovered from illegal step
            is_done = True
            continue

        new_state = tic_tac_toe.take_step(action_tuple, state)
        new_state_representation = state_to_str(new_state)

        if tic_tac_toe.is_leaf(new_state):
            reward = tic_tac_toe.goodness(new_state, 'X')
            print("Game Over - Result: ", "X wins" if reward == 1 else "O wins" if reward == -1 else "Draw")
            tic_tac_toe.print(new_state)
            is_done = True

        state = new_state.copy()
        state_representation = new_state_representation
        if state_representation not in state_to_id:
            state_to_id[state_representation] = len(state_to_id)

        if is_done:
            break

        # Human player's turn
        print("Current board state: ")
        tic_tac_toe.print(state)
        inp = input("Your choice (x-y):").split("-")
        pos_x, pos_y = int(inp[0]), int(inp[1])
        human_step = (pos_x, pos_y)

        if human_step not in state['steps']:
            print("Invalid move, position is already taken. Try again.")
            continue

        state = tic_tac_toe.take_step(human_step, state)
        state_representation = state_to_str(state)
        if state_representation not in state_to_id:
            state_to_id[state_representation] = len(state_to_id)

        if tic_tac_toe.is_leaf(state):
            reward = tic_tac_toe.goodness(state, "X")
            print("Game Over. Final Result: ", "You win" if reward == 1 else "You lose" if reward == -1 else "Draw")
            is_done = True


if __name__ == '__main__':
    main()

