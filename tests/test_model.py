from game_of_life.model import GridCorner, MatrixData


class TestModel:
    def setup_method(self, method):
        self.og_grid_corner = GridCorner(top_left=(0, 0), bottom_right=(5, 6))
        self.grid = MatrixData([(1, 1), (1, 0), (1, 2)])

    def test_neighbours(self):
        cell = (0, 0)
        neighbours = sorted(
            [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        )
        fn_neighbours = sorted(MatrixData.neighbours(cell, distance=1))
        assert neighbours == fn_neighbours

    def test_step_one_afar(self):
        grid_corner = MatrixData.step_one_afar(self.og_grid_corner)
        assert grid_corner.top_left == (-1, -1)
        assert grid_corner.bottom_right == (6, 7)

    def test_new_grid_corner_outside(self):
        cell = (-1, -1)
        grid_corner = MatrixData.new_grid_corner(cell, self.og_grid_corner)
        assert grid_corner.top_left == cell
        assert grid_corner.bottom_right == self.og_grid_corner.bottom_right

    def test_new_grid_corner_inside(self):
        cell = (2, 1)
        grid_corner = MatrixData.new_grid_corner(cell, self.og_grid_corner)
        assert grid_corner.top_left == self.og_grid_corner.top_left
        assert grid_corner.bottom_right == self.og_grid_corner.bottom_right

    def test_current_alive_cells(self):
        self.grid.data[(1, 3)] = 1
        assert sorted(self.grid.current_alive_cells()) == sorted(
            [(1, 1), (1, 0), (1, 2), (1, 3)]
        )
