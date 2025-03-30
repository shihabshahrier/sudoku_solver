import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import time

class SudokuSolver:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.original_grid = np.array(grid)
        self.steps = []
        self.fig = None
        self.ax = None
        self.ani = None
    
    def is_valid(self, row, col, num):
        # Check row
        if num in self.grid[row, :]:
            return False
        
        # Check column
        if num in self.grid[:, col]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        if num in self.grid[box_row:box_row+3, box_col:box_col+3]:
            return False
        
        return True
    
    def find_empty(self):
        # Find an empty cell (with 0)
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    return (i, j)
        return None
    
    def solve(self):
        # Find empty cell
        empty_cell = self.find_empty()
        
        # No empty cells left, we're done
        if not empty_cell:
            return True
        
        row, col = empty_cell
        
        # Try digits 1-9
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                # Place the number
                self.grid[row, col] = num
                
                # Record this step
                self.steps.append((row, col, num, True))
                
                # Recursively solve the rest
                if self.solve():
                    return True
                
                # If we get here, we need to backtrack
                self.grid[row, col] = 0
                self.steps.append((row, col, 0, False))
        
        return False
    
    def visualize_solution(self, speed=200):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        
        def update(frame):
            if frame < len(self.steps):
                row, col, num, success = self.steps[frame]
                self.draw_grid()
                
                # Highlight the cell being considered
                if success:
                    color = 'limegreen'
                else:
                    color = 'tomato'
                
                rect = plt.Rectangle((col, 8-row), 1, 1, fill=True, alpha=0.5, color=color)
                self.ax.add_patch(rect)
                
                # Show the number
                if num != 0:
                    self.ax.text(col+0.5, 8-row+0.5, str(num), 
                                 fontsize=18, ha='center', va='center',
                                 color='blue' if success else 'red')
                
                # Update title with step info
                action = "Place" if success else "Backtrack"
                self.ax.set_title(f"Step {frame+1}/{len(self.steps)}: {action} {num} at ({row+1},{col+1})")
            else:
                self.draw_grid(final=True)
                self.ax.set_title("Solved Sudoku Puzzle")
        
        self.ani = FuncAnimation(self.fig, update, frames=len(self.steps)+1, interval=speed, repeat=False)
        plt.show()
    
    def draw_grid(self, final=False):
        self.ax.clear()
        
        # Draw grid lines
        for i in range(10):
            lw = 2 if i % 3 == 0 else 0.5
            self.ax.axhline(i, color='black', lw=lw)
            self.ax.axvline(i, color='black', lw=lw)
            
        # Fill original numbers
        for i in range(9):
            for j in range(9):
                if self.original_grid[i, j] != 0:
                    self.ax.text(j+0.5, 8-i+0.5, str(self.original_grid[i, j]), 
                                 fontsize=18, ha='center', va='center', color='black', weight='bold')
                elif final and self.grid[i, j] != 0:
                    self.ax.text(j+0.5, 8-i+0.5, str(self.grid[i, j]), 
                                 fontsize=18, ha='center', va='center', color='blue')
        
        self.ax.set_xlim(0, 9)
        self.ax.set_ylim(0, 9)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
    
    def solve_and_visualize(self, speed=200):
        self.steps = []
        start_time = time.time()
        if self.solve():
            solve_time = time.time() - start_time
            print(f"Puzzle solved in {solve_time:.2f} seconds!")
            print(f"Solution steps: {len(self.steps)}")
            self.visualize_solution(speed)
        else:
            print("No solution exists for this puzzle.")


# Example usage
if __name__ == "__main__":
    # Example puzzle (0 represents empty cells)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    solver = SudokuSolver(puzzle)
    solver.solve_and_visualize(speed=1)  # Lower values = faster animation