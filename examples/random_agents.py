import gym
import numpy as np

environment = gym.make('gym_spoof:spoof-v0')
number_heads, coin_layout = environment.reset(shuffle_initial=True)
done = False
current_turn = 0
environment.render()
while not done:
    print(f"player {current_turn}'s turn")
    player_0_action, player_1_action = environment.action_space.sample()
    print(f"player 0 chooses to flip coin at index: {np.argmax(player_0_action)}\nplayer 1 chooses to {'not ' if not player_1_action else ''}swap the other two coins")
    world_state, rewards, done, info = environment.step((player_0_action, player_1_action))
    
    environment.render()
    #print(world_state, rewards, done, info)
    current_turn = info['next_turn']
