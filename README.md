# gym-spoof
OpenAI Gym for a variation on the zero-sum game "spoof", otherwise known as "The 3-coin game"

!["Two figures playing the 3-coin game with each other"](/assets/spoof.png "The 3-coin game")

Games with Imperfect Information: Theory and Algorithms (Laurent Doyen and Jean-Fran ̧cois Raskin)

## About Spoof
Spoof, otherwise known as "The 3-coin game" is a multi-agent, imperfect-information, zero-sum game.
# Premise
Three coins are arranged on a table, either head or tail up.  
E.g: `(Head, Head, Tail)`

Player 0 only knows the number of heads which are up, Player 0 does not get to see the coins directly.  
E.g: `2`

Player 1 knows the full state of all the coins.  
E.g. `(Head, Head, Tail)`

Player 0's objective is to get the coins into a configuration where they are all "heads-up" while Player 1's objective is getting all coins into a "tails-up" configuartion.  
**Spoof is a two-player zero-sum game**, therefore, a win for Player 0 is equvillant to a loss for Player 1

E.g. `(Head, Head, Head)` *Player 0 wins* & *Player 1 loses*  
E.g. `(Tail, Tail, Tail)` *Player 1 wins* & *Player 0 loses*

# How to play
1. Player 1 chooses a configuaration of the 3 coins, consisting of 2 heads and 1 tail.  
E.g. `(Head, Tail, Head)`
2. Player 0 chooses 1 coin in the set, without knowing whether it's heads or tails, and asks Player 1 to toggle that coin.  
E.g. Player 0 chooses to toggle the first coin:  
`(Tail, Tail, Head)`
3. Player 1 can, but is not required, to exchange the positions of the two coins which were not flipped.  
E.g. Player 1 chooses to swap the positions:  
`(Tail, Head, Tail)`
4. Player 1 tells Player 0 how many heads are up.  
E.g. `1`
5. Steps 2-4 are repeated until all coins are "heads-up", in which case Player 0 wins, or until all coins are "tails-up" and Player 1 wins.

---

## Installation
Installs like any other custom Gym environment.
```
git clone https://github.com/MouseAndKeyboard/gym-spoof.git
cd gym-spoof
pip install -e .
```
## Usage
```python
import gym
environment = gym.make('gym_spoof:spoof-v0')
# Multi-agent environments return multiple observation states in a tuple.
(player_0_observation, player_1_observation) = environment.reset(shuffle_initial=True) #Initial configuration of coins is randomised

# Which player is going to make their move
active_player = 0
```
Multi-agent environments make use of the "Tuple" gym space type for actions and observations.  
The custom "Categorical" action space type is a One-Hot vector, where the hot element refers to the coin Player 0 wants to flip
```python
self.action_space = spaces.Tuple(
    (
        categorical_space.Categorical(self.coin_count),
        spaces.Discrete(2)
    )
)
```

```python
done = False
player_0_action = None
player_1_action = None
while not done:
    if active_player == 0:
        # choose to flip the second coin
        player_0_action = [0, 1, 0]

        # choose to flip the third coin
        #player_0_action = [0, 0, 1]
    else:
        # Swap the coins not flipped by Player 0
        player_1_action = True 

        # Don't swap the coins not flipped by Player 0
        # player_1_action = False

    world_state, rewards, done, info = environment.step((player_0_action, player_1_action))

    player_0_observation, player_1_observation = world_state
    player_0_reward, player_1_reward = rewards

    # who's turn is it to act? Player 0 or Player 1
    active_player = info['next_turn']

```
`./examples/` provides some sample implementations of the gym.
