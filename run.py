from typing import List

from .model import Cell, MatrixData
from .the_game import Game

if __name__ == "__main__":
    alive_cells: List[Cell] = []
    for _ in range(int(input())):
        raw_coordinates = input()
        coordinates = list(map(int, raw_coordinates.split()))
        alive_cells.append((coordinates[0], coordinates[1]))
    data = MatrixData(alive_cells)
    game = Game(data, use_conn_comp=True)
    game.run_step()
    print(data)
