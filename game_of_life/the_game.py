from typing import Callable, DefaultDict, Iterable, List, Optional, Set

from .model import Cell, GridCorner, MatrixData
from .state_functions import state_functions


class Game:

    """
    Game:
    This is the place which plays the game, changes the alive-dead values

    data_clean: keeps track if the data is clean or not
    (dirty data means cells stores info of more than one state)

    state_functions: rules through which cells die or are born

    use_conn_comp: uses connected-components-method if set True
    """

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

    """
    run_step: Plays one step of Game-of-Life
    """

    def run_step(self) -> None:
        assert self.data_clean
        if self.use_conn_comp:
            for comp_grid_corner in self._find_disconnected_components():
                # fill next states for all independent disconnected components
                self._fill_next_state(comp_grid_corner)
        else:
            grid_corner = self._find_max_alive_box()
            if grid_corner is not None:
                self._fill_next_state(grid_corner)

    """
    _fill_next_state: Stores the next states in the cells in the given grid-area
    (makes the data dirty, but cleans up at the end)
    """

    def _fill_next_state(self, grid_corners: GridCorner) -> None:
        assert self.data_clean
        self.data_clean = False
        for i in range(grid_corners.top_left[0], grid_corners.bottom_right[0] + 1):
            for j in range(grid_corners.top_left[1], grid_corners.bottom_right[1] + 1):
                cell = (i, j)
                live_neighbours = self._live_neighbours_count(cell)
                for state_function in self.state_functions:
                    new_alive_state = state_function(
                        bool(self.data[cell]), live_neighbours
                    )
                    if new_alive_state is not None:
                        self.data[cell] |= int(new_alive_state) << 1
                        self._update_alive_cell_set(cell, new_alive_state)
                        break
        self._clean_data(grid_corners)

    """
    _update_alive_cell_set: If using connected-components-method,
    updates the alive-state of the current cell
    """

    def _update_alive_cell_set(self, cell: Cell, alive: bool) -> None:
        if self.use_conn_comp:
            if alive:
                self.alive_cell_set.add(cell)
            elif cell in self.alive_cell_set:
                self.alive_cell_set.remove(cell)

    """
    _find_disconnected_components: Finds disconnected components using DFS
    """

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

    """
    _find_max_alive_box: If there is any alive cell in the data,
    it returns the minimal-sized grid-area encapsulating all alive cells
    """

    def _find_max_alive_box(self) -> Optional[GridCorner]:
        assert self.data_clean
        grid_corner: Optional[GridCorner] = None
        for cell, is_alive in self.data.items():
            if is_alive:
                grid_corner = MatrixData.new_grid_corner(cell, grid_corner)
        if grid_corner is None:
            return None
        return MatrixData.step_one_afar(grid_corner)

    """
    _live_neighbours_count: Returns count of neighbours for the cell
    which are alive
    """

    def _live_neighbours_count(self, cell: Cell) -> int:
        live = 0
        for neighbour in MatrixData.neighbours(cell, distance=1):
            live += self.data[neighbour] & 1
        return live

    """
    _clean_data: Cleans up the previous stored state
    """

    def _clean_data(self, grid_corners: GridCorner) -> None:
        if self.data_clean:
            return
        for i in range(grid_corners.top_left[0], grid_corners.bottom_right[0] + 1):
            for j in range(grid_corners.top_left[1], grid_corners.bottom_right[1] + 1):
                cell = (i, j)
                self.data[cell] >>= 1
        self.data_clean = True
