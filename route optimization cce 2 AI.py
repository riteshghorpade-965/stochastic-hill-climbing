import tkinter as tk
from tkinter import messagebox
import random


class StochasticHillClimbingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stochastic Hill Climbing - Path Finding")
        self.root.geometry("1200x750")
        self.root.resizable(False, False)

        # Data
        self.states = {}
        self.graph = {}
        self.positions = {}
        self.path = []
        self.current = None
        self.goal = None
        self.running = False

        # -------------------------------
        # TITLE
        # -------------------------------
        title = tk.Label(
            root,
            text="STOCHASTIC HILL CLIMBING",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            root,
            text="User-Based Path Finding with Random Better-Neighbor Selection",
            font=("Arial", 11)
        )
        subtitle.pack()

        # -------------------------------
        # INPUT FRAME
        # -------------------------------
        input_frame = tk.Frame(root, relief="groove", bd=2)
        input_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(
            input_frame,
            text="INPUT",
            font=("Arial", 15, "bold")
        ).pack(pady=10)

        # Start
        tk.Label(input_frame, text="Start State:").pack(anchor="w", padx=10)

        self.start_entry = tk.Entry(input_frame, width=25)
        self.start_entry.pack(padx=10, pady=5)

        # Goal
        tk.Label(input_frame, text="Goal State:").pack(anchor="w", padx=10)

        self.goal_entry = tk.Entry(input_frame, width=25)
        self.goal_entry.pack(padx=10, pady=5)

        # Number of states
        tk.Label(
            input_frame,
            text="Number of States:"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.number_entry = tk.Entry(input_frame, width=25)
        self.number_entry.pack(padx=10, pady=5)

        # State values
        tk.Label(
            input_frame,
            text="States & Values\nExample: A 1"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.states_text = tk.Text(
            input_frame,
            width=28,
            height=7
        )
        self.states_text.pack(padx=10, pady=5)

        # Neighbors
        tk.Label(
            input_frame,
            text="Neighbors\nExample: A: B C"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.neighbor_text = tk.Text(
            input_frame,
            width=28,
            height=8
        )
        self.neighbor_text.pack(padx=10, pady=5)

        # Buttons
        tk.Button(
            input_frame,
            text="CREATE GRAPH",
            width=22,
            command=self.create_graph
        ).pack(pady=8)

        tk.Button(
            input_frame,
            text="START SEARCH",
            width=22,
            command=self.start_search
        ).pack(pady=5)

        tk.Button(
            input_frame,
            text="RESET",
            width=22,
            command=self.reset
        ).pack(pady=5)

        # -------------------------------
        # GRAPH AREA
        # -------------------------------
        graph_frame = tk.Frame(root, relief="groove", bd=2)
        graph_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tk.Label(
            graph_frame,
            text="SEARCH GRAPH",
            font=("Arial", 15, "bold")
        ).pack(pady=5)

        self.canvas = tk.Canvas(
            graph_frame,
            width=850,
            height=600,
            bg="white"
        )
        self.canvas.pack(padx=5, pady=5)

        # Status
        self.status = tk.Label(
            root,
            text="Enter data and click CREATE GRAPH",
            font=("Arial", 12, "bold")
        )
        self.status.pack(side="bottom", pady=8)

    # ==========================================================
    # CREATE GRAPH
    # ==========================================================

    def create_graph(self):

        try:
            self.states = {}
            self.graph = {}
            self.path = []

            start = self.start_entry.get().strip()
            goal = self.goal_entry.get().strip()

            if not start or not goal:
                messagebox.showerror(
                    "Error",
                    "Please enter Start State and Goal State."
                )
                return

            self.current = start
            self.goal = goal

            # Number of states
            n = int(self.number_entry.get())

            # Read states and values
            lines = self.states_text.get("1.0", tk.END).strip().splitlines()

            if len(lines) != n:
                messagebox.showerror(
                    "Error",
                    f"Please enter exactly {n} states."
                )
                return

            for line in lines:
                parts = line.split()

                if len(parts) != 2:
                    messagebox.showerror(
                        "Error",
                        "Use format: A 1"
                    )
                    return

                state = parts[0]
                value = float(parts[1])

                self.states[state] = value
                self.graph[state] = []

            # Check start and goal
            if start not in self.states:
                messagebox.showerror(
                    "Error",
                    "Start State is not present in states."
                )
                return

            if goal not in self.states:
                messagebox.showerror(
                    "Error",
                    "Goal State is not present in states."
                )
                return

            # Read neighbors
            neighbor_lines = (
                self.neighbor_text
                .get("1.0", tk.END)
                .strip()
                .splitlines()
            )

            for line in neighbor_lines:

                if not line.strip():
                    continue

                if ":" not in line:
                    messagebox.showerror(
                        "Error",
                        "Use format: A: B C"
                    )
                    return

                state, neighbors = line.split(":", 1)

                state = state.strip()
                neighbors = neighbors.strip()

                if state not in self.graph:
                    messagebox.showerror(
                        "Error",
                        f"Unknown state: {state}"
                    )
                    return

                if neighbors:
                    neighbor_list = neighbors.split()

                    for neighbor in neighbor_list:

                        if neighbor not in self.states:
                            messagebox.showerror(
                                "Error",
                                f"Unknown neighbor: {neighbor}"
                            )
                            return

                        # Do not add self as neighbor
                        if neighbor != state:
                            self.graph[state].append(neighbor)

            # Calculate positions
            self.calculate_positions()

            # Draw graph
            self.draw_graph()

            self.status.config(
                text="Graph created successfully. Click START SEARCH."
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter valid numbers."
            )

    # ==========================================================
    # POSITION CALCULATION
    # ==========================================================

    def calculate_positions(self):

        self.positions = {}

        states = list(self.states.keys())

        # Predefined positions for easy demo
        predefined = {
            "A": (150, 100),
            "B": (350, 200),
            "C": (350, 50),
            "D": (550, 300),
            "E": (550, 100),
            "F": (550, 450),
            "G": (750, 250)
        }

        for i, state in enumerate(states):

            if state in predefined:
                self.positions[state] = predefined[state]

            else:
                x = 150 + (i % 4) * 180
                y = 100 + (i // 4) * 180

                self.positions[state] = (x, y)

    # ==========================================================
    # DRAW GRAPH
    # ==========================================================

    def draw_graph(self):

        self.canvas.delete("all")

        # Draw edges first
        for state in self.graph:

            x1, y1 = self.positions[state]

            for neighbor in self.graph[state]:

                x2, y2 = self.positions[neighbor]

                self.canvas.create_line(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="gray",
                    width=2,
                    arrow=tk.LAST
                )

        # Draw nodes
        for state in self.states:

            x, y = self.positions[state]

            radius = 35

            # Goal
            if state == self.goal:
                outline = "green"
                width = 4

            else:
                outline = "black"
                width = 2

            self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill="white",
                outline=outline,
                width=width,
                tags=f"node_{state}"
            )

            self.canvas.create_text(
                x,
                y - 8,
                text=state,
                font=("Arial", 16, "bold")
            )

            self.canvas.create_text(
                x,
                y + 15,
                text=f"Value: {self.states[state]}",
                font=("Arial", 9)
            )

        # Goal label
        if self.goal in self.positions:

            x, y = self.positions[self.goal]

            self.canvas.create_text(
                x,
                y - 55,
                text="🎯 GOAL",
                font=("Arial", 11, "bold"),
                fill="green"
            )

    # ==========================================================
    # START SEARCH
    # ==========================================================

    def start_search(self):

        if not self.graph:
            messagebox.showerror(
                "Error",
                "Please create the graph first."
            )
            return

        if self.running:
            return

        self.running = True
        self.current = self.start_entry.get().strip()
        self.goal = self.goal_entry.get().strip()
        self.path = [self.current]

        self.status.config(
            text=f"Starting from {self.current}..."
        )

        self.animate_step()

    # ==========================================================
    # STOCHASTIC HILL CLIMBING
    # ==========================================================

    def animate_step(self):

        current = self.current

        # Goal reached
        if current == self.goal:

            self.running = False

            self.highlight_final_path()

            self.status.config(
                text=f"🎯 GOAL REACHED!   Path: {' → '.join(self.path)}"
            )

            return

        current_value = self.states[current]

        neighbors = self.graph.get(current, [])

        # No neighbors
        if not neighbors:

            self.running = False

            self.status.config(
                text=f"❌ No neighbors from {current}. Search stopped."
            )

            return

        # Better neighbors
        better_neighbors = []

        for neighbor in neighbors:

            if self.states[neighbor] > current_value:
                better_neighbors.append(neighbor)

        # No better neighbor
        if not better_neighbors:

            self.running = False

            self.status.config(
                text=f"⚠️ No better neighbor from {current}. Search stopped."
            )

            return

        # Random selection
        next_state = random.choice(better_neighbors)

        # Update status
        self.status.config(
            text=(
                f"Current: {current} ({current_value})   "
                f"→   Randomly selected: "
                f"{next_state} ({self.states[next_state]})"
            )
        )

        # Highlight current -> next
        self.highlight_move(current, next_state)

        self.current = next_state
        self.path.append(next_state)

        # Continue after delay
        self.root.after(1500, self.animate_step)

    # ==========================================================
    # HIGHLIGHT MOVE
    # ==========================================================

    def highlight_move(self, current, next_state):

        x1, y1 = self.positions[current]
        x2, y2 = self.positions[next_state]

        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="blue",
            width=5,
            arrow=tk.LAST
        )

        # Highlight current node
        self.canvas.create_oval(
            x1 - 35,
            y1 - 35,
            x1 + 35,
            y1 + 35,
            outline="blue",
            width=4
        )

        # Highlight next node
        self.canvas.create_oval(
            x2 - 35,
            y2 - 35,
            x2 + 35,
            y2 + 35,
            outline="orange",
            width=4
        )

    # ==========================================================
    # FINAL PATH
    # ==========================================================

    def highlight_final_path(self):

        # Redraw original graph
        self.draw_graph()

        # Draw final path
        for i in range(len(self.path) - 1):

            current = self.path[i]
            next_state = self.path[i + 1]

            x1, y1 = self.positions[current]
            x2, y2 = self.positions[next_state]

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="blue",
                width=6,
                arrow=tk.LAST
            )

        # Highlight path nodes
        for state in self.path:

            x, y = self.positions[state]

            self.canvas.create_oval(
                x - 38,
                y - 38,
                x + 38,
                y + 38,
                outline="blue",
                width=5
            )

        # Goal
        x, y = self.positions[self.goal]

        self.canvas.create_text(
            x,
            y + 55,
            text="🎯 GOAL REACHED!",
            font=("Arial", 11, "bold"),
            fill="green"
        )

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self.states = {}
        self.graph = {}
        self.positions = {}
        self.path = []
        self.current = None
        self.goal = None
        self.running = False

        self.canvas.delete("all")

        self.start_entry.delete(0, tk.END)
        self.goal_entry.delete(0, tk.END)
        self.number_entry.delete(0, tk.END)
        self.states_text.delete("1.0", tk.END)
        self.neighbor_text.delete("1.0", tk.END)

        self.status.config(
            text="Enter data and click CREATE GRAPH"
        )


# ==============================================================
# MAIN PROGRAM
# ==============================================================

root = tk.Tk()

app = StochasticHillClimbingGUI(root)

root.mainloop()
