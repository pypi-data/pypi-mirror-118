import numpy as np
import gym
from gym.error import ResetNeeded

from pogema.fast_grid import FastGrid, random_grid_generator
from pogema.grid_config import GridConfig


class SingleAgentPogema(gym.Env):

    def __init__(self, config: GridConfig = GridConfig(num_agents=1)):
        # noinspection PyTypeChecker
        self.grid: FastGrid = None
        self.config = config

        full_size = self.config.obs_radius * 2 + 1
        self.observation_space = gym.spaces.Box(0.0, 1.0, shape=(3, full_size, full_size))
        self.action_space = gym.spaces.Discrete(len(self.config.MOVES))

    def step(self, action):
        self.check_reset()

        finish = self.grid.move(0, action)
        info = dict()
        reward = 1.0 if finish else 0.0
        return self._get_obs(), reward, finish, info

    def _get_obs(self, agent_id=0):
        return np.concatenate([
            self.grid.get_obstacles(agent_id)[None],
            self.grid.get_positions(agent_id)[None],
            self.grid.get_square_target(agent_id)[None]
        ])

    def _get_obs_dict(self, agent_id=0):
        observation = dict(
            obs=np.concatenate([
                self.grid.get_obstacles(agent_id)[None],
                self.grid.get_positions(agent_id)[None],
                self.grid.get_square_target(agent_id)[None]
            ]),
            target_vector=self.grid.get_target(agent_id)
        )
        return observation

    def reset(self):
        self.grid: FastGrid = random_grid_generator(config=self.config)
        return self._get_obs()

    def check_reset(self):
        if self.grid is None:
            raise ResetNeeded("Please reset environment first!")

    def render(self, mode='human'):
        self.check_reset()
        return self.grid.render(mode=mode)


class MultiAgent(gym.Env):
    def __init__(self):
        pass


def main():
    env = gym.make('SingleAgentPogema-v0', )
    env.reset()
    for _ in range(100):
        _, _, done, _ = env.step(env.action_space.sample())
        env.render()
        if done:
            break


if __name__ == '__main__':
    main()
