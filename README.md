# Game of Life

The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead. Every cell interacts with its eight neighbours, which are the cells that are directly horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

1. Any live cell with fewer than two live neighbours dies, as if by loneliness.
2. Any live cell with more than three live neighbours dies, as if by overcrowding.
3. Any live cell with two or three live neighbours lives, unchanged, to the next generation.
4. Any dead cell with exactly three live neighbours comes to life.

The initial pattern constitutes the 'seed' of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed - births and deaths happen simultaneously, and the discrete moment at which this happens is sometimes called a tick. (In other words, each generation is a pure function of the one before.) The rules continue to be applied repeatedly to create further generations.

## Solution

This seems very simplistic and straightforward problem at first, but when thought about, is very interesting and intriguing. Through the following sections, I'll elaborate what I have implemented in the code and what was the thought process behind everything.

### The most obvious solution
We've been given a grid. Every cell's state is coming from nine cells: eight neighbours and one itself - that too from the previous step. The cells in a particular state don't affect each other, until used for obtaining next step.

The obvious solution over here is to just create an empty grid of the same given size whose cells' values will come from the given grid. This can easily be done by creating a 2-D array (new_array) and filling the values by iterating over its cells.

```new_array[i][j] = F(array[i][j], count_of_alive_neighbours)```

Here ***F()*** is a function which gives value according to the given rules.
In the code, these functions are defined in [state_functions.py](./game_of_life/state_functions.py).

### Infinite-ness
I need a data-structure to hold the values of the matrix. 2-D array seemed an obvious choice, but the problem states that it's ***infinite two-dimensional orthogonal grid***.

Although over here we're only required to answer next step, but in case we're required to answer more than 1 step-run in future, it would be problematic - as seen from the test cases already, there can be oscillating patterns. So, if the values are populated near the edges and are lost in one step-run in case it overran the boundary, it won't be usable for the following step.

So I can't rely on arrays with fixed length, I need an extendable list. Moreover it can stretch to negative index as well - in all four quadrants. Maintaining it would be a hassle. I chose a simple data structure to hold the values - a Hashmap.

```map[cell] -> 0/1``` (0 for Dead, 1 for Alive)

In the code, this data structure is defined in [model.py](./game_of_life/model.py) as **`MatrixData.data`**

### "GridCorner"

In the same [model.py](./game_of_life/model.py), I've defined a **`GridCorner`** class. Now that I have the hash map, I need to get the matrix boundaries to iterate over. `GridCorner` stores the `top_left` and `bottom_right` cell locations of the grid I want in any case.

### Identifying connected components
A cell can affect another cell for next state at most distance a distance of 1 (neighbour). So if we have a group of alive cells connected together, they may only change cells in the range which form the periphery of those connected cells, just one layer out of them. A group of dead cells remain dead (remain unchanged).

If these group of cells are far apart in our grid, iterating all the cells for scanning the values to be changed isn't worth it, because we know a large parts of groups of dead cells will remain dead. So if we identify these group of alive cells and consider these groups one by one in our focus, we can prune large portions of the grid for search-space.

This optimization is exactly what I've added under Game's `use_conn_comp` bool variable in the constructor. When set true, this will use `_find_disconnected_components` to find connected components which then returns list of `GridCorner` as the focus areas we should target.

To identify these groups of alive cells, I've used standard DFS (Depth-First-Search). But to do this, I'd need to maintain the set cells which are alive at all times, which may take O(n^2) space in worst case.

### Space Optimizations
This is another optimization which I've added in the default step-run implementation. As mentioned in the *most obvious solution* section above, I could have created another empty data structure to store values for the next state. I thought what if I can do it in-place, so it wouldn't require that humongous extra space.

The problem is that if I'm iterating in top-to-down left-to-right order to fill values, I'll lose the previous state's values for the neighbours in the upper row and the left neighbour. So I thought of storing both the state's values in each cell.

So, something like `data[(i,j)] = "Alive, Dead"` denoting that in previous state, this cell was dead, and in this state, this cell is alive.

When used live and dead's notation as discussed in previous section, looks like "00", "01", "10", and "11" which look like the binary numbers with just two bits - which is very compact. As such, I've kept the data-type of map as:
```map[cell] -> (int)```

Now, iterating in top-to-down left-to-right order to fill values has no issues as I can access the previous state value any time. Once I've done this iteration, I can clean away the previous state values, keeping only the current state values.

This code is written in [game.py](./game_of_life/the_game.py)

### Trade offs and Conclusion

I found connected-components thing as a very good optimization for grids with sparse groups for alive cells - but this comes at a cost of extra space. Now, I could think of ways in which I could use it or not in the time vs space trade-off depending on the alive sparse-ness of the grid, but that was going out of scope. So I've added that just as an extension (configurable with just setting a bool), so that it can be compared, if tested out.

## How to run

### Dependencies
The project would need at least Python version 3.8 to run.

### Running the code
```$ python -m game_of_life.run```

#### Input Format
First line: integer 'n' - containing the number of alive cells
Next n lines are the space seperated coordinates of alive-cells

```
3
1 0
1 1
1 2
```

#### Config:
Edit the [run.py](./game_of_life/run.py) to change **`USE_CONNECTED_COMPONENTS_METHOD`** `True` or `False`.

### Running the tests

You can install the test dependencies through:

```$ pip install -r requirements.txt```

OR from `pyproject.toml` or `poetry.lock`.

**Run the tests by running:**

```$ pytest```

### Dev-Dependencies
I've used multiple libraries for linting like `black`, `autoflake` and `isort` and libraries to check coverage for type-hints like `mypy` which can be checked out in pyproject.toml file under dev-dependencies.
