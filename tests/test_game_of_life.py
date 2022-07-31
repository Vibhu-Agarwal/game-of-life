from game_of_life.model import GridCorner, MatrixData
from game_of_life.the_game import Game


class TestGame:
    def setup_method(self, method):
        self.alive_cells = [(1, 1), (1, 0), (1, 2)]
        self.grid = MatrixData(self.alive_cells)
        self.answer = sorted([(1, 1), (0, 1), (2, 1)])

    def test_init_std(self):
        game = Game(self.grid)
        assert game.data_clean
        assert not game.use_conn_comp

    def test_init_conn_comp(self):
        game = Game(self.grid, use_conn_comp=True)
        assert game.data_clean
        assert game.use_conn_comp

    def test_live_neighbours_count(self):
        game = Game(self.grid)
        assert game._live_neighbours_count((1, 1)) == 2

    def test_max_box_alive(self):
        game = Game(self.grid)
        assert game._find_max_alive_box() == GridCorner(
            top_left=(0, -1), bottom_right=(2, 3)
        )

    def test_one_disconn_comp(self):
        game = Game(self.grid, use_conn_comp=True)
        assert len(list(game._find_disconnected_components())) == 1

    def test_two_disconn_comp(self):
        self.grid = MatrixData([(1, 1), (1, 0), (1, 2), (5, 5)])
        game = Game(self.grid, use_conn_comp=True)
        assert len(list(game._find_disconnected_components())) == 2

    def test_answer_std(self):
        game = Game(self.grid)
        game.run_step()
        assert self.answer == self.grid.current_alive_cells(sort=True)

    def test_answer_conn_comp(self):
        self.grid = MatrixData([(1, 1), (1, 0), (1, 2), (5, 5)])
        game = Game(self.grid, use_conn_comp=True)
        game.run_step()
        assert self.answer == self.grid.current_alive_cells(sort=True)
