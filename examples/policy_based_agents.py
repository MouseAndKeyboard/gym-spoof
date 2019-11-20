import gym
import numpy as np


a = False
b = False
def player_0_policy(history):
    global a
    global b
    # perform some calculation based on what's happened up until this point
    if a:
        a = not a
        return np.array([0,0,1])
    else:
        a = not a
        if b:
            b = not b
            return np.array([1,0,0])
        else:
            b = not b
            return np.array([0,1,0])
        

def player_1_policy(history):
    # perform some calculation based on what's happened up until this point
    return True

environment = gym.make('gym_spoof:spoof-v0')

EPISODES = 20

for i in range(EPISODES):
    old_world_state = environment.reset(initial_state=[True, True, False], shuffle_initial=True)
    done = False
    current_turn = 0
    print('----------------------------------------------')
    environment.render()

    player_0_history = []
    player_1_history = []
    player_0_action = None
    player_1_action = None
    while not done:
        print(f"player {current_turn}'s turn")
        # player 1 will act deterministically, based on the policy defined
        if current_turn == 0:
            player_0_action = player_0_policy(player_0_history)
            print(f"player 0 chooses to flip coin at index: {np.argmax(player_0_action)}")
            new_world_state, rewards, done, info = environment.step((player_0_action, player_1_action))
              
        else:
            player_1_action = player_1_policy(player_1_history)
            print(f"player 1 chooses to {'not ' if not player_1_action else ''}swap the other two coins")
            new_world_state, rewards, done, info = environment.step((player_0_action, player_1_action))
                    
        
        environment.render()

        current_turn = info['next_turn']
        old_world_state = new_world_state
