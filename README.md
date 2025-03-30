# Sudoku Solver

This repository contains two Python-based Sudoku solvers:

1. **`sudoku.py`**: A solver with a visualization of the solving process using Matplotlib animations.
2. **`sudoku2.py`**: An interactive Sudoku solver with a graphical interface that allows users to input puzzles, solve them, and step through the solution process.

## Features

### `sudoku.py`
- Solves Sudoku puzzles using a backtracking algorithm.
- Visualizes the solving process step-by-step with animations.
- Highlights cells being filled or backtracked.
- Displays the final solved puzzle.

### `sudoku2.py`
- Provides an interactive graphical interface for solving Sudoku puzzles.
- Allows users to:
  - Input numbers into the grid.
  - Clear cells or reset the puzzle.
  - Load an example puzzle.
  - Solve the puzzle and step through the solution process.
- Highlights the solving process with color-coded actions (placement and backtracking).
- Displays instructions and status updates in the interface.

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `numpy`
  - `matplotlib`

Install the required libraries using pip:

```bash
pip install numpy matplotlib
```

## Usage

### Running `sudoku.py`
1. Open a terminal and navigate to the repository directory.
2. Run the script:

   ```bash
   python sudoku.py
   ```

3. The script will solve a predefined Sudoku puzzle and visualize the solving process.

### Running `sudoku2.py`
1. Open a terminal and navigate to the repository directory.
2. Run the script:

   ```bash
   python sudoku2.py
   ```

3. Use the graphical interface to:
   - Input numbers into the grid.
   - Solve the puzzle.
   - Step through the solution process.
   - Reset or clear the puzzle.

## Example Puzzle

The example puzzle used in both scripts:

```
5 3 0 | 0 7 0 | 0 0 0
6 0 0 | 1 9 5 | 0 0 0
0 9 8 | 0 0 0 | 0 6 0
------+-------+------
8 0 0 | 0 6 0 | 0 0 3
4 0 0 | 8 0 3 | 0 0 1
7 0 0 | 0 2 0 | 0 0 6
------+-------+------
0 6 0 | 0 0 0 | 2 8 0
0 0 0 | 4 1 9 | 0 0 5
0 0 0 | 0 8 0 | 0 7 9
```

## Screenshots

### `sudoku.py` Visualization
![Sudoku Solver Visualization](https://via.placeholder.com/800x400?text=Sudoku+Solver+Visualization)

### `sudoku2.py` Interactive Interface
![Interactive Sudoku Solver](https://via.placeholder.com/800x400?text=Interactive+Sudoku+Solver)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The backtracking algorithm is a classic approach to solving Sudoku puzzles.
- Matplotlib is used for visualization and creating the interactive interface.

Happy solving!
