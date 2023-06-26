import pprint

from pathlib import Path


class _Config:

    def __init__(self):
        self.root_dir = Path(__file__).parents[1].resolve()
        self.package_dir = self.root_dir / 'src'
        self.data_dir = self.root_dir / 'data'
        self.output_dir = self.root_dir / 'output'

    def __repr__(self):
        return pprint.pformat(vars(self))


config = _Config()