from typing import Callable, DefaultDict, Iterable, List, Optional, Set

from .model import Cell, GridCorner, MatrixData
from .state_functions import state_functions


class Game:

    data: DefaultDict[Cell, int]
    data_clean: bool
    state_functions: List[Callable[[bool, int], Optional[bool]]]
    use_conn_comp: bool

    def __init__(self, data: MatrixData, use_conn_comp=False):
        self.data = data.data
        self.data_clean = True
        self.state_functions = state_functions()
        self.use_conn_comp = use_conn_comp
        if self.use_conn_comp:
            self.alive_cell_set: Set[Cell] = set(data.current_alive_cells())

    def run_step(self) -> None:
        assert self.data_clean
        if self.use_conn_comp:
            for comp_grid_corner in self._find_disconnected_components():
                self._fill_next_state(comp_grid_corner)
        else:
            grid_corner = self._find_max_alive_box()
            if grid_corner is not None:
                self._fill_next_state(grid_corner)

    def _fill_next_state(self, grid_corners: GridCorner) -> None:
        assert self.data_clean
        self.data_clean = False
        for i in range(grid_corners.top_left[0], grid_corners.bottom_right[0] + 1):
            for j in range(grid_corners.top_left[1], grid_corners.bottom_right[1] + 1):
                cell = (i, j)
                live_neighbours = self._live_neighbours_count(cell, grid_corners)
                for state_function in self.state_functions:
                    new_alive_state = state_function(
                        bool(self.data[cell]), live_neighbours
                    )
                    if new_alive_state is not None:
                        self.data[cell] |= int(new_alive_state) << 1
                        self._update_alive_cell_set(cell, new_alive_state)
                        break
        self._clean_data(grid_corners)

    def _update_alive_cell_set(self, cell: Cell, alive: bool) -> None:
        if self.use_conn_comp:
            if alive:
                self.alive_cell_set.add(cell)
            elif cell in self.alive_cell_set:
                self.alive_cell_set.remove(cell)

    def _find_disconnected_components(self) -> Iterable[GridCorner]:
        assert self.data_clean
        disconnected_comps: List[GridCorner] = []
        visited = set()

        def dfs(cell: Cell, append_new: bool) -> None:
            if cell in visited:
                return
            visited.add(cell)
            if append_new:
                disconnected_comps.append(GridCorner(cell, cell))
            else:
                disconnected_comps[-1] = MatrixData.new_grid_corner(
                    cell, disconnected_comps[-1]
                )
            for neighbour in MatrixData.neighbours(cell, distance=2):
                if self.data[neighbour]:
                    dfs(neighbour, False)

        for alive_cell in self.alive_cell_set:
            dfs(alive_cell, True)
        return map(
            lambda grid_corner: MatrixData.step_one_afar(grid_corner),
            disconnected_comps,
        )

    def _find_max_alive_box(self) -> Optional[GridCorner]:
        assert self.data_clean
        grid_corner: Optional[GridCorner] = None
        for cell, is_alive in self.data.items():
            if is_alive:
                grid_corner = MatrixData.new_grid_corner(cell, grid_corner)
        if grid_corner is None:
            return None
        return MatrixData.step_one_afar(grid_corner)

    def _live_neighbours_count(self, cell: Cell, grid_corners: GridCorner) -> int:
        assert not self.data_clean
        live = 0
        for neighbour in MatrixData.neighbours(
            cell, grid_corners=grid_corners, distance=1
        ):
            live += self.data[neighbour] & 1
        return live - (self.data[cell] & 1)

    def _clean_data(self, grid_corners: GridCorner) -> None:
        if self.data_clean:
            return
        for i in range(grid_corners.top_left[0], grid_corners.bottom_right[0] + 1):
            for j in range(grid_corners.top_left[1], grid_corners.bottom_right[1] + 1):
                cell = (i, j)
                self.data[cell] >>= 1
        self.data_clean = True
