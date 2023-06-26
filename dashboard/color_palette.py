from typing import List


class ColorPalette:
    def __init__(self):
        self.idx = 0

    def __getitem__(self, index: int):
        return self._colors[index % len(self._colors)]

    def __len__(self):
        return len(self._colors)

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        try:
            return self._colors[self.idx - 1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    def set_colors(self, colors: List[str]):
        self._colors = colors


color_palette = ColorPalette()
