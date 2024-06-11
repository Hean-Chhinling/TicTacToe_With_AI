import numpy
import random


class QLearningAgent:
    def __init__(self, n_states, n_actions, learning_rate):
        self.n_states = n_states
        self.n_actions = n_actions
        self.learning_rate = learning_rate

        self.q_table = numpy.random.rand(n_states, n_actions)  # q-table initial value

    def act(self, state, epsilon):
        random_int = random.uniform(0, 1)

        if random_int > epsilon:
            action = numpy.argmax(self.q_table[state])
        else:
            action = random.randint(0, self.n_actions - 1)

        return action

    def learn(self, state, action, reward, new_state, gamma):
        old_value = self.q_table[state][action]
        new_state = reward + gamma*max(self.q_table[new_state])

        self.q_table[state][action] = old_value + self.learning_rate*(new_state - old_value)
