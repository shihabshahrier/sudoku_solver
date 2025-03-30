import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import time
import copy

class InteractiveSudokuSolver:
    def __init__(self):
        self.grid = np.zeros((9, 9), dtype=int)
        self.original_grid = np.zeros((9, 9), dtype=int)
        self.solution_states = []
        self.current_state_index = -1
        self.selected_cell = None
        self.solving = False
        self.solved = False
        
        # Set up the figure and axes
        plt.style.use('ggplot')
        self.fig = plt.figure(figsize=(12, 9))
        self.gs = self.fig.add_gridspec(12, 12)
        
        # Main grid area
        self.ax_grid = self.fig.add_subplot(self.gs[0:9, 0:9])
        
        # Button areas
        ax_num_buttons = [self.fig.add_subplot(self.gs[9, i]) for i in range(9)]
        ax_solve = self.fig.add_subplot(self.gs[10, 0:3])
        ax_reset = self.fig.add_subplot(self.gs[10, 3:6])
        ax_clear = self.fig.add_subplot(self.gs[10, 6:9])
        ax_prev = self.fig.add_subplot(self.gs[11, 0:3])
        ax_next = self.fig.add_subplot(self.gs[11, 3:6])
        ax_example = self.fig.add_subplot(self.gs[11, 6:9])
        
        # Status area
        self.ax_status = self.fig.add_subplot(self.gs[0:5, 9:12])
        
        # Create number buttons (1-9)
        self.num_buttons = [Button(ax, str(i+1)) for i, ax in enumerate(ax_num_buttons)]
        for i, button in enumerate(self.num_buttons):
            button.on_clicked(lambda event, num=i+1: self.place_number(num))
        
        # Create control buttons
        self.solve_button = Button(ax_solve, 'Solve')
        self.solve_button.on_clicked(self.start_solving)
        
        self.reset_button = Button(ax_reset, 'Reset')
        self.reset_button.on_clicked(self.reset_puzzle)
        
        self.clear_button = Button(ax_clear, 'Clear')
        self.clear_button.on_clicked(self.clear_selection)
        
        self.prev_button = Button(ax_prev, 'Previous')
        self.prev_button.on_clicked(self.previous_state)
        
        self.next_button = Button(ax_next, 'Next')
        self.next_button.on_clicked(self.next_state)
        
        self.example_button = Button(ax_example, 'Load Example')
        self.example_button.on_clicked(self.load_example)
        
        # Set up the grid interactivity
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Initialize the grid
        self.draw_grid()
        self.update_status()
        
        plt.tight_layout()
    
    def on_click(self, event):
        if event.inaxes == self.ax_grid and not self.solving:
            col = int(event.xdata) if event.xdata < 9 else 8
            row = 8 - int(event.ydata) if event.ydata < 9 else 0
            
            if 0 <= row < 9 and 0 <= col < 9:
                self.selected_cell = (row, col)
                self.draw_grid()
                self.update_status()
    
    def place_number(self, num):
        if self.selected_cell and not self.solving:
            row, col = self.selected_cell
            
            # Only allow changing cells that aren't part of the original puzzle
            # during solving process
            if self.solved:
                # Don't modify when viewing solution
                return
            elif self.original_grid[row, col] == 0 or not np.any(self.original_grid):
                self.grid[row, col] = num
                self.draw_grid()
                self.update_status()
    
    def clear_selection(self, event=None):
        if self.selected_cell and not self.solving and not self.solved:
            row, col = self.selected_cell
            
            # Only allow clearing cells that aren't part of the original puzzle
            # or if we haven't started solving yet
            if self.original_grid[row, col] == 0 or not np.any(self.original_grid):
                self.grid[row, col] = 0
                self.draw_grid()
                self.update_status()
    
    def update_status(self):
        self.ax_status.clear()
        self.ax_status.axis('off')
        
        # Display status information
        if self.selected_cell:
            row, col = self.selected_cell
            status_text = f"Selected cell: ({row+1}, {col+1})"
        else:
            status_text = "Click on a cell to select it"
        
        if self.solving:
            status_text += "\nSolving puzzle..."
        elif self.solved:
            status_text += f"\nPuzzle solved! ({len(self.solution_states)} steps)"
            if self.current_state_index >= 0:
                status_text += f"\nViewing step {self.current_state_index+1}/{len(self.solution_states)}"
        
        self.ax_status.text(0.05, 0.95, status_text, 
                          transform=self.ax_status.transAxes,
                          fontsize=12, verticalalignment='top')
        
        # Display instructions
        instructions = [
            "Instructions:",
            "1. Click a cell to select it",
            "2. Click a number button (1-9) to place it",
            "3. Use 'Clear' to remove a number",
            "4. Click 'Solve' to solve the puzzle",
            "5. Use 'Previous'/'Next' to step through solution",
            "6. Use 'Reset' to start over",
            "7. Use 'Load Example' for a sample puzzle"
        ]
        
        y_pos = 0.7
        for line in instructions:
            self.ax_status.text(0.05, y_pos, line, 
                              transform=self.ax_status.transAxes,
                              fontsize=10, verticalalignment='top')
            y_pos -= 0.05
        
        self.fig.canvas.draw_idle()
    
    def draw_grid(self):
        self.ax_grid.clear()
        
        # Draw grid lines
        for i in range(10):
            lw = 2 if i % 3 == 0 else 0.5
            self.ax_grid.axhline(i, color='black', lw=lw)
            self.ax_grid.axvline(i, color='black', lw=lw)
        
        # Draw cell highlight if a cell is selected
        if self.selected_cell:
            row, col = self.selected_cell
            rect = plt.Rectangle((col, 8-row), 1, 1, fill=True, alpha=0.3, color='skyblue')
            self.ax_grid.add_patch(rect)
        
        # Draw numbers in the grid
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] != 0:
                    if self.original_grid[i, j] != 0:
                        color = 'black'
                        weight = 'bold'
                    else:
                        color = 'blue'
                        weight = 'normal'
                    
                    self.ax_grid.text(j+0.5, 8-i+0.5, str(self.grid[i, j]), 
                                    fontsize=18, ha='center', va='center', 
                                    color=color, weight=weight)
        
        self.ax_grid.set_xlim(0, 9)
        self.ax_grid.set_ylim(0, 9)
        self.ax_grid.set_aspect('equal')
        self.ax_grid.set_title('Sudoku Puzzle')
        self.ax_grid.axis('off')
        
        self.fig.canvas.draw_idle()
    
    def is_valid(self, grid, row, col, num):
        # Check row
        if num in grid[row, :]:
            return False
        
        # Check column
        if num in grid[:, col]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        if num in grid[box_row:box_row+3, box_col:box_col+3]:
            return False
        
        return True
    
    def find_empty(self, grid):
        # Find an empty cell (with 0)
        for i in range(9):
            for j in range(9):
                if grid[i, j] == 0:
                    return (i, j)
        return None
    
    def solve_algorithm(self, grid):
        # Find empty cell
        empty_cell = self.find_empty(grid)
        
        # No empty cells left, we're done
        if not empty_cell:
            return True
        
        row, col = empty_cell
        
        # Try digits 1-9
        for num in range(1, 10):
            if self.is_valid(grid, row, col, num):
                # Place the number
                grid[row, col] = num
                
                # Record this state
                state = {
                    'grid': copy.deepcopy(grid),
                    'row': row,
                    'col': col,
                    'num': num,
                    'action': 'place'
                }
                self.solution_states.append(state)
                
                # Recursively solve the rest
                if self.solve_algorithm(grid):
                    return True
                
                # If we get here, we need to backtrack
                grid[row, col] = 0
                
                # Record this backtrack state
                state = {
                    'grid': copy.deepcopy(grid),
                    'row': row,
                    'col': col,
                    'num': num,
                    'action': 'backtrack'
                }
                self.solution_states.append(state)
        
        return False
    
    def start_solving(self, event):
        if not self.solving and not self.solved:
            # Save the original grid
            self.original_grid = np.copy(self.grid)
            self.solution_states = []
            self.current_state_index = -1
            
            # Start solving
            self.solving = True
            self.update_status()
            
            # Solve in a non-blocking way
            plt.pause(0.1)  # Give the UI a chance to update
            
            start_time = time.time()
            success = self.solve_algorithm(np.copy(self.grid))
            solve_time = time.time() - start_time
            
            if success:
                print(f"Puzzle solved in {solve_time:.2f} seconds!")
                print(f"Solution steps: {len(self.solution_states)}")
                self.solved = True
                if len(self.solution_states) > 0:
                    self.show_state(len(self.solution_states)-1)  # Show the final state
            else:
                print("No solution exists for this puzzle.")
            
            self.solving = False
            self.update_status()
    
    def show_state(self, index):
        if 0 <= index < len(self.solution_states):
            state = self.solution_states[index]
            self.grid = np.copy(state['grid'])
            
            # Highlight the changed cell
            self.selected_cell = (state['row'], state['col'])
            
            # Draw the grid
            self.draw_grid()
            
            # Add a colored rectangle to indicate placement or backtracking
            row, col = state['row'], state['col']
            color = 'limegreen' if state['action'] == 'place' else 'tomato'
            rect = plt.Rectangle((col, 8-row), 1, 1, fill=True, alpha=0.3, color=color)
            self.ax_grid.add_patch(rect)
            
            # Update the title
            action = "Place" if state['action'] == 'place' else "Backtrack"
            self.ax_grid.set_title(f"Step {index+1}/{len(self.solution_states)}: {action} {state['num']} at ({row+1},{col+1})")
            
            self.current_state_index = index
            self.update_status()
    
    def previous_state(self, event):
        if self.solved and self.current_state_index > 0:
            self.show_state(self.current_state_index - 1)
    
    def next_state(self, event):
        if self.solved and self.current_state_index < len(self.solution_states) - 1:
            self.show_state(self.current_state_index + 1)
    
    def reset_puzzle(self, event):
        # Reset everything
        self.grid = np.zeros((9, 9), dtype=int)
        self.original_grid = np.zeros((9, 9), dtype=int)
        self.solution_states = []
        self.current_state_index = -1
        self.selected_cell = None
        self.solving = False
        self.solved = False
        
        self.draw_grid()
        self.update_status()
        
        # Ensure the title is reset
        self.ax_grid.set_title('Sudoku Puzzle')
        self.fig.canvas.draw_idle()

    def load_example(self, event=None):
        # Reset first to clear any existing state
        self.reset_puzzle(None)
        
        # Load a sample puzzle
        example = [
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
        self.grid = np.array(example)
        # Don't set original_grid yet - we only set it when solving begins
        
        self.draw_grid()
        self.update_status()

    def run(self):
        plt.show()


if __name__ == "__main__":
    app = InteractiveSudokuSolver()
    app.load_example()
    app.run()