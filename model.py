from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Iterable, Iterator, List, Optional, Tuple

Cell = Tuple[int, int]


@dataclass
class GridCorner:
    top_left: Cell
    bottom_right: Cell


class MatrixData:
    def __init__(self, alive_cells: List[Cell]):
        self.data: DefaultDict[Cell, int] = defaultdict(int)
        for point in alive_cells:
            self.data[point] = 1

    def current_alive_cells(self, *, sort=False) -> Iterable[Cell]:
        alive_cells = filter(lambda cell: self.data[cell] & 1, self.data.keys())
        return sorted(alive_cells) if sort else alive_cells

    def __str__(self) -> str:
        display = ""
        for cell in self.current_alive_cells(sort=True):
            display += f"{', '.join(map(str, cell))}\n"
        return display

    @classmethod
    def new_grid_corner(
        cls, cell: Cell, grid_corner: Optional[GridCorner]
    ) -> GridCorner:
        if grid_corner is None:
            return GridCorner(cell, cell)
        else:
            top_left = grid_corner.top_left
            bottom_right = grid_corner.bottom_right
            if (cell[0] < top_left[0]) or (cell[1] < top_left[1]):
                top_left = (min(top_left[0], cell[0]), min(top_left[1], cell[1]))
            if (cell[0] > bottom_right[0]) or (cell[1] > bottom_right[1]):
                bottom_right = (
                    max(bottom_right[0], cell[0]),
                    max(bottom_right[1], cell[1]),
                )
            return GridCorner(top_left, bottom_right)

    @classmethod
    def step_one_afar(cls, grid_corners: GridCorner) -> GridCorner:
        top_left = (grid_corners.top_left[0] - 1, grid_corners.top_left[1] - 1)
        bottom_right = (
            grid_corners.bottom_right[0] + 1,
            grid_corners.bottom_right[1] + 1,
        )
        return GridCorner(top_left, bottom_right)

    @classmethod
    def neighbours(
        cls, cell: Cell, *, grid_corners: Optional[GridCorner] = None, distance: int
    ) -> Iterator[Cell]:
        row_start, row_end = cell[0] - distance, cell[0] + distance
        col_start, col_end = cell[1] - distance, cell[1] + distance
        if grid_corners is not None:
            mnr, mnc = grid_corners.top_left
            mxr, mxc = grid_corners.bottom_right
            row_start, row_end = max(row_start, mnr), min(row_end, mxr)
            col_start, col_end = max(col_start, mnc), min(col_end, mxc)
        for i in range(row_start, 1 + row_end):
            for j in range(col_start, 1 + col_end):
                yield i, j
