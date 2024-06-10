import pickle

from tictactoe import TicTacToe, random_player, state_to_str
from game_search_algorithms import QLearningAgent
from tqdm import tqdm
import numpy


agent = QLearningAgent(n_states=19683, n_actions=9, learning_rate=0.01)  # 3^9 = 19683
tic_tac_toe = TicTacToe()
state_to_id = {}


def play_episodes(n_episodes, max_epsilon=1.0, min_epsilon=0.05, decay_rate=0.0001, gamma=0.9, learn=True, enemy=None):
    rewards = []
    epsilon_history = []

    for episode in tqdm(range(n_episodes)):
        is_done = False

        epsilon = min_epsilon + (max_epsilon - min_epsilon)*numpy.exp(-decay_rate*episode)  # epsilon exponential decay formula
        total_reward = 0
        state = tic_tac_toe.initial
        state_representation = state_to_str(state)
        if state_representation not in state_to_id:
            state_to_id[state_representation] = len(state_to_id)

        while not is_done:
            action = agent.act(state=state_to_id[state_representation], epsilon=epsilon)
            action_tuple = ((action // 3) + 1, (action % 3) + 1)  # convert the action (0-8) into a (row, column) tuple
            new_state = tic_tac_toe.take_step(state=state, step=action_tuple)
            state_representation = state_to_str(state)
            new_state_representation = state_to_str(new_state)

            if tic_tac_toe.is_leaf(new_state):
                reward = tic_tac_toe.goodness(new_state, 'X')  # 1, -1 or 0
                is_done = True
            elif new_state_representation == state_representation:
                reward = -1
                is_done = True
            else:
                reward = 0

            if state_representation not in state_to_id:
                state_to_id[state_representation] = len(state_to_id)
            if new_state_representation not in state_to_id:
                state_to_id[new_state_representation] = len(state_to_id)

            if learn:
                agent.learn(state_to_id[state_representation], action, reward, state_to_id[new_state_representation],
                            gamma)
            total_reward += reward
            state = new_state.copy()

            if is_done:
                break

            # The enemy's turn
            step = enemy(tic_tac_toe, state)
            state = tic_tac_toe.take_step(step, state)

            if tic_tac_toe.is_leaf(state):
                reward = tic_tac_toe.goodness(state, "X")
                total_reward += reward
                agent.learn(state_to_id[state_representation], action, reward,
                            state_to_id[new_state_representation], gamma)
                state_representation = state_to_str(state)  # TODO
                break

            state_representation = state_to_str(state)
            if state_representation not in state_to_id:
                state_to_id[state_representation] = len(state_to_id)

        if not learn and total_reward < 0:
            print(state_representation)
            print("Total reward: ", total_reward)

        rewards.append(total_reward)
        epsilon_history.append(epsilon)

    return rewards, epsilon_history


# Train the agent
rewards, epsilon_history = play_episodes(n_episodes=1000_000, max_epsilon=1.0, min_epsilon=0.05,
                                         decay_rate=0.0001, gamma=0.9, learn=True, enemy=random_player)


def main():

    print("Summary Statistics after training: ")
    print("Wins: ", len([r for r in rewards if r > 0]))
    print("Loses: ", len([r for r in rewards if r < 0]))
    print("Ties: ", len([r for r in rewards if r == 0]))

    # Save the agent
    with open("tic_tac_toe_agent.pkl", "wb") as f:
        pickle.dump(agent, f)
    with open("state_to_id.pkl", "wb") as f:
        pickle.dump(state_to_id, f)


if __name__ == '__main__':
    main()











