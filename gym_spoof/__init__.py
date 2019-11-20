from gym.envs.registration import register

register(
    id='spoof-v0',
    entry_point='gym_spoof.envs:SpoofEnv',
)