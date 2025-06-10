import tkinter as tk
from tkinter import messagebox
from floodfill import FloodFillAlgorithm 


class FloodFillUI:
    def __init__(self, width=30, height=20):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.start = None
        self.end = None
        self.mode = "wall"  # "wall", "start", "end"
        self.running = False

        # Colors
        self.colors = {
            0: "white",      # empty
            1: "black",      # wall
            2: "green",      # start
            3: "red",        # end
            4: "lightblue",  # visited
            5: "yellow"      # path
        }

        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Flood Fill Algorithm Visualizer")
        self.root.resizable(False, False)

        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        # Mode buttons
        tk.Label(control_frame, text="Mode:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)

        self.wall_btn = tk.Button(control_frame, text="Wall", bg="lightgray",
                                    command=lambda: self.set_mode("wall"))
        self.wall_btn.grid(row=0, column=1, padx=2)

        self.start_btn = tk.Button(control_frame, text="Start", bg="lightgreen",
                                    command=lambda: self.set_mode("start"))
        self.start_btn.grid(row=0, column=2, padx=2)

        self.end_btn = tk.Button(control_frame, text="End", bg="lightcoral",
                                command=lambda: self.set_mode("end"))
        self.end_btn.grid(row=0, column=3, padx=2)

        # Algorithm selection
        tk.Label(control_frame, text="Algorithm:", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=(20,5))
        self.algorithm_var = tk.StringVar(value="bfs")
        algorithm_menu = tk.OptionMenu(control_frame, self.algorithm_var, "bfs", "dfs")
        algorithm_menu.config(width=8, bg="lightsteelblue")
        algorithm_menu.grid(row=0, column=5, padx=2)

        # Action buttons
        tk.Label(control_frame, text="Actions:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=(10,0))

        self.run_btn = tk.Button(control_frame, text="Run Algorithm", bg="lightblue",
                                command=self.run_flood_fill)
        self.run_btn.grid(row=1, column=1, padx=2, pady=(10,0))

        self.clear_btn = tk.Button(control_frame, text="Clear Grid", bg="lightyellow",
                                    command=self.clear_grid)
        self.clear_btn.grid(row=1, column=2, padx=2, pady=(10,0))

        self.reset_btn = tk.Button(control_frame, text="Reset Search", bg="lightpink",
                                    command=self.reset_search)
        self.reset_btn.grid(row=1, column=3, padx=2, pady=(10,0))

        # Speed control
        tk.Label(control_frame, text="Speed:", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=(10,0))
        self.speed_var = tk.IntVar(value=50)
        speed_scale = tk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                variable=self.speed_var, length=200)
        speed_scale.grid(row=2, column=1, columnspan=3, pady=(10,0))

        # Algorithm info label
        self.info_label = tk.Label(control_frame, text="BFS: Shortest path guaranteed", font=("Arial", 9), fg="blue")
        self.info_label.grid(row=2, column=4, columnspan=2, pady=(10,0))
        
        # Update info when algorithm changes
        self.algorithm_var.trace('w', self.update_algorithm_info)

        # Canvas
        self.canvas = tk.Canvas(self.root, width=self.width * self.cell_size, height=self.height * self.cell_size, bg="white")
        self.canvas.pack(pady=10)

        # Draw grid
        self.draw_grid()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # Instructions
        instructions = tk.Label(self.root,
                                text="Instructions: Select mode, click to place walls/start/end, choose algorithm, then run!",
                                font=("Arial", 10), fg="gray")
        instructions.pack(pady=5)

    def update_algorithm_info(self, *args):
        """Update the algorithm information label"""
        algorithm = self.algorithm_var.get()
        if algorithm == "bfs":
            self.info_label.config(text="BFS: Shortest path guaranteed", fg="blue")
        else:
            self.info_label.config(text="DFS: Explores depth first", fg="darkgreen")

    def draw_grid(self):
        self.canvas.delete("all")

        # Draw cells
        for y in range(self.height):
            for x in range(self.width):
                x1, y1 = x * self.cell_size, y * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                color = self.colors[self.grid[y][x]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

        # Draw grid lines
        for i in range(self.width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.height * self.cell_size, fill="gray")

        for i in range(self.height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.width * self.cell_size, y, fill="gray")

    def set_mode(self, mode):
        self.mode = mode
        # Update button appearances
        self.wall_btn.config(relief="raised")
        self.start_btn.config(relief="raised")
        self.end_btn.config(relief="raised")

        if mode == "wall":
            self.wall_btn.config(relief="sunken")
        elif mode == "start":
            self.start_btn.config(relief="sunken")
        elif mode == "end":
            self.end_btn.config(relief="sunken")

    def on_click(self, event):
        if self.running:
            return
        self.handle_cell_click(event.x, event.y)

    def on_drag(self, event):
        if self.running:
            return
        self.handle_cell_click(event.x, event.y)

    def handle_cell_click(self, x, y):
        grid_x = x // self.cell_size
        grid_y = y // self.cell_size

        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            if self.mode == "wall":
                if self.grid[grid_y][grid_x] not in [2, 3]:  # Don't overwrite start/end
                    self.grid[grid_y][grid_x] = 1 if self.grid[grid_y][grid_x] != 1 else 0
            elif self.mode == "start":
                # Clear previous start
                if self.start:
                    self.grid[self.start[1]][self.start[0]] = 0
                self.grid[grid_y][grid_x] = 2
                self.start = (grid_x, grid_y)
            elif self.mode == "end":
                # Clear previous end
                if self.end:
                    self.grid[self.end[1]][self.end[0]] = 0
                self.grid[grid_y][grid_x] = 3
                self.end = (grid_x, grid_y)

            self.draw_grid()

    def clear_grid(self):
        if self.running:
            return
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.start = None
        self.end = None
        self.draw_grid()

    def reset_search(self):
        if self.running:
            return
        # Keep walls, start, and end, but clear visited cells
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] in [4, 5]:  # visited or path
                    self.grid[y][x] = 0
        self.draw_grid()

    def get_speed(self):
        return (101 - self.speed_var.get()) / 1000.0

    def run_flood_fill(self):
        if self.running:
            return

        if not self.start or not self.end:
            messagebox.showwarning("Warning", "Please set both start and end points!")
            return

        self.running = True
        self.run_btn.config(state="disabled")

        # Reset previous search
        self.reset_search()

        # Get selected algorithm
        selected_algorithm = self.algorithm_var.get()

        # Run flood fill algorithm
        algo = FloodFillAlgorithm(
            self.grid,
            self.start,
            self.end,
            selected_algorithm,
            speed_callback=self.get_speed,
            update_callback=lambda: [self.draw_grid(), self.root.update()]
        )
        path_found = algo.search()

        algorithm_name = "BFS" if selected_algorithm == "bfs" else "DFS"
        if path_found:
            messagebox.showinfo("Success", f"Path found using {algorithm_name}!")
        else:
            messagebox.showinfo("No Path", f"No path exists between start and end using {algorithm_name}!")

        self.running = False
        self.run_btn.config(state="normal")

    def run(self):
        # Set initial mode
        self.set_mode("wall")
        self.root.mainloop()