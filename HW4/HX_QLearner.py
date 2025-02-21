"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

import numpy as np
import pandas as pd
import time


class QLearningTable:

    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, verbose=False):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        # self.epsilon = epsilon
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)      # Initialize S
        self.new_state_counter = 0
        self.verbose = verbose

    def choose_action(self, observation, epsilon):
        self.check_state_exist(observation)
        # action selection
        if np.random.random() > epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action

            action = np.random.randint(len(self.actions))

            action = np.random.choice(self.actions)
            # print(self.actions)
            # action = 0

        return action

    def learn(self, s, a, r, s_, alpha):   # learning for Q learning table
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        # self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update , Morvan's original
        self.q_table.loc[s, a] += alpha * (q_target - q_predict)  # update , HX self defined
        if self.verbose >= 2:
            print('\n Q table is:\n', self.q_table)

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.new_state_counter += 1
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )
            if self.verbose >= 1:
                print('========adding', self.new_state_counter,'th new state====== : ', state)
            if self.verbose >= 2:
                print('\n Q table is:\n', self.q_table)


    def return_Q_table(self):
        return self.q_table