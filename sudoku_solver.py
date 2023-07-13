import tkinter as tk
import random
import time

# Constants
WINDOW_SIZE = 540
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
FONT = ("Arial", 20)
DIFFICULTY_LEVELS = {
    "Easy": 30,
    "Medium": 40,
    "Hard": 50
}

# Initialize Tkinter
root = tk.Tk()
root.title("Sudoku Solver")

# Variables
selected_cell = None
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
original_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
solution = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
start_time = 0
elapsed_time = 0
timer_running = False

def generate_sudoku(difficulty):
    # Create an empty Sudoku grid
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Fill diagonal 3x3 subgrids
    for i in range(0, GRID_SIZE, 3):
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(digits)
        for j in range(3):
            for k in range(3):
                grid[i + j][i + k] = digits.pop()

    # Solve the Sudoku grid
    solve_sudoku(grid)

    # Remove cells to create the desired difficulty level
    remove_cells(grid, DIFFICULTY_LEVELS[difficulty])

    return grid


def solve_sudoku(grid):
    # Find empty cell
    empty_cell = find_empty_cell(grid)
    if empty_cell is None:
        return True

    row, col = empty_cell

    # Try placing numbers from 1 to 9
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            # Place the number if it's valid
            grid[row][col] = num

            # Recursively solve the Sudoku grid
            if solve_sudoku(grid):
                return True

            # Reset the cell if no solution found
            grid[row][col] = 0

    return False


def find_empty_cell(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return (row, col)
    return None


def is_valid_move(grid, row, col, num):
    # Check if the number exists in the row
    if num in grid[row]:
        return False

    # Check if the number exists in the column
    for i in range(GRID_SIZE):
        if grid[i][col] == num:
            return False

    # Check if the number exists in the 3x3 subgrid
    subgrid_start_row = (row // 3) * 3
    subgrid_start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[subgrid_start_row + i][subgrid_start_col + j] == num:
                return False

    return True


def draw_grid():
    canvas.delete("all")
    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            line_width = 2
        else:
            line_width = 1
        canvas.create_line(0, i * CELL_SIZE, WINDOW_SIZE, i * CELL_SIZE, width=line_width)
        canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, WINDOW_SIZE, width=line_width)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_value = grid[i][j]
            if cell_value != 0:
                if original_grid[i][j] == 0:
                    color = "black"
                else:
                    color = "blue"
                canvas.create_text(
                    j * CELL_SIZE + CELL_SIZE // 2,
                    i * CELL_SIZE + CELL_SIZE // 2,
                    text=str(cell_value),
                    font=FONT,
                    fill=color
                )
            else:
                entry = tk.Entry(canvas, justify="center", font=FONT, width=2)
                entry.insert(0, str(cell_value))
                entry.bind("<Key>", number_entry_key_pressed)
                entry.bind("<FocusIn>", lambda event, row=i, col=j: entry_focus_in(row, col))
                entry.bind("<FocusOut>", entry_focus_out)
                canvas.create_window(
                    j * CELL_SIZE + CELL_SIZE // 2,
                    i * CELL_SIZE + CELL_SIZE // 2,
                    window=entry,
                    tags="entry"
                )


def draw_solution():
    canvas.delete("solution")
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_value = solution[i][j]
            if cell_value != 0:
                canvas.create_text(
                    j * CELL_SIZE + CELL_SIZE // 2,
                    i * CELL_SIZE + CELL_SIZE // 2,
                    text=str(cell_value),
                    font=FONT,
                    fill="blue",
                    tags="solution"
                )


def generate_button_click():
    global grid, original_grid, selected_cell, start_time, elapsed_time, timer_running
    selected_cell = None
    start_time = time.time()
    elapsed_time = 0
    timer_running = True
    difficulty = difficulty_menu.get()
    grid = generate_sudoku(difficulty)
    original_grid = [[grid[i][j] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    draw_grid()


def solve_button_click():
    global grid, solution, selected_cell, timer_running, elapsed_time
    selected_cell = None
    timer_running = False
    elapsed_time = 0
    for i in range(GRID_SIZE):
        solution[i] = grid[i][:]
    solve_sudoku(solution)
    draw_solution()


def cell_clicked(event):
    global selected_cell
    row = event.y // CELL_SIZE
    col = event.x // CELL_SIZE
    selected_cell = (row, col)
    draw_grid()


def number_entry_key_pressed(event):
    global selected_cell
    if selected_cell:
        row, col = selected_cell
        if grid[row][col] != 0:  # Allow changes for previously entered values
            if event.char.isdigit():
                num = int(event.char)
                if 1 <= num <= 9:
                    grid[row][col] = num
                    draw_grid()



def entry_focus_in(row, col):
    global selected_cell
    selected_cell = (row, col)


def entry_focus_out(event):
    global selected_cell
    selected_cell = None


def remove_cells(grid, num_cells):
    cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
    random.shuffle(cells)
    for i in range(num_cells):
        row, col = cells[i]
        grid[row][col] = 0
def solve_button_click():
    global grid, solution, selected_cell, timer_running, elapsed_time
    selected_cell = None
    timer_running = False
    elapsed_time = 0
    for i in range(GRID_SIZE):
        solution[i] = grid[i][:]
    solve_sudoku(solution)
    draw_solution()
    canvas.delete("entry")  # Remove the entry fields to display the solution
      
def update_timer():
    global elapsed_time
    if timer_running:
        elapsed_time = time.time() - start_time
        timer_label.config(text="Timer: {:.2f} seconds".format(elapsed_time))
    root.after(100, update_timer)  # Remove parentheses after update_timer


# Create canvas
canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE)
canvas.pack()

# Create buttons
generate_button = tk.Button(root, text="Generate", command=generate_button_click)
generate_button.pack(side="left", padx=10, pady=10)
solve_button = tk.Button(root, text="Solve", command=solve_button_click)
solve_button.pack(side="left", padx=10, pady=10)

# Create difficulty level selector
difficulty_label = tk.Label(root, text="Difficulty Level:")
difficulty_label.pack(side="left", padx=10, pady=10)

difficulty_menu = tk.StringVar(root)
difficulty_menu.set("Easy")  # Set the default difficulty level

difficulty_option_menu = tk.OptionMenu(root, difficulty_menu, *DIFFICULTY_LEVELS.keys())
difficulty_option_menu.pack(side="left", padx=10, pady=10)

# Create timer label
timer_label = tk.Label(root, text="Timer: 0.00 seconds")
timer_label.pack(side="right", padx=10, pady=10)

# Bind mouse and keyboard events
canvas.bind("<Button-1>", cell_clicked)
root.bind("<Key>", number_entry_key_pressed)

# Start the timer
update_timer()

# Generate initial Sudoku
generate_button_click()

# Start the Tkinter event loop
root.mainloop()
