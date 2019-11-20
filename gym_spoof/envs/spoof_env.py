import gym
from gym import error, spaces, utils
from gym.utils import seeding
import gym_spoof.utils.categorical_space as categorical_space
import numpy as np
import random


class SpoofEnv(gym.Env):
  metadata = {'render.modes': ['human']}


  def __init__(self):
    self.coin_count = 3
    self.n_agents = 2
    self.player_0_turn = True
    self.coin_state = random.shuffle([True, True, False])
    # n coins c_1, c_2, ..., c_(n-1), c_n) 
    # are arranged on a table, either head up (TRUE) or tail up (FALSE).
    self.observation_space = spaces.Tuple(
      (
        spaces.Discrete(self.coin_count + 1),
        spaces.MultiBinary(self.coin_count)
      )
    )

    self.action_space = spaces.Tuple(
      (
        categorical_space.Categorical(self.coin_count),
        spaces.Discrete(2)
      )
    )

  def getObservations(self):
    return (np.count_nonzero(self.coin_state), self.coin_state)

  def allHeads(self):
    return np.count_nonzero(self.coin_state) == 3

  def allTails(self):
    return np.count_nonzero(self.coin_state) == 0

  def step(self, action):
    if self.player_0_turn:
      assert np.count_nonzero(action[0]) == 1
      # flip the specified coin
      self.coin_state[np.argmax(action[0])] = not self.coin_state[np.argmax(action[0])]

    else:
      # swap the coins
      if action[1]:
        
        a = np.argmax(action[0])
        swap1 = (a + 1) % self.coin_count
        swap2 = (a + self.coin_count - 1) % self.coin_count

        temp = self.coin_state[swap1]
        self.coin_state[swap1] = self.coin_state[swap2]
        self.coin_state[swap2] = temp

    reward = (0, 0)
    done = False
    if self.allHeads():
      done = True
      reward = (1, -1)
    if self.allTails():
      done = True
      reward = (-1, 1)

    self.player_0_turn = not self.player_0_turn
    return self.getObservations(), reward, done, {'next_turn': 0 if self.player_0_turn else 1}

  def reset(self, initial_state=[True, True, False], shuffle_initial=False):
    if shuffle_initial:
      random.shuffle(initial_state)
    assert np.count_nonzero(initial_state) == 2
    self.coin_state = initial_state
    return self.getObservations()

  def render(self, mode='human'):
    for coin in self.coin_state:
      if coin:
        print('H', end='')
      else:
        print('T', end='')
    print()

