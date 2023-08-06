from gym import register

from pogema.grid_config import GridConfig

__version__ = '0.1'

__all__ = [
    'GridConfig',
]

register(
    id="SingleAgentPogema-v0",
    entry_point="pogema.envs:SingleAgentPogema",
    max_episode_steps=32,
)
