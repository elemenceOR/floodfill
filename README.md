# Flood Fill Algorithm Visualizer

A Python-based desktop visualizer for the **Flood Fill (BFS)** pathfinding algorithm using **Tkinter**. Build mazes, place start/end points, and watch the algorithm in action with adjustable speed and a user-friendly GUI.

## Features

- Click-to-draw walls, start, and end points on a grid
- Real-time visualization of the BFS flood fill algorithm
- Adjustable animation speed
- Reset search or clear the grid easily
- Fully interactive UI using `tkinter`

## How It Works

This project implements **Breadth-First Search (BFS)** to find the shortest path from a start to an end cell on a 2D grid with walls as obstacles. It shows:
- Visited nodes (`lightblue`)
- Final path (`yellow`)
- Live updates while the algorithm runs

## Screenshot
![image](https://github.com/user-attachments/assets/2daf4e05-f42e-46b1-9e4a-25f7a432b230)

## Getting Started

### Requirements

- Python 3.x
- Tkinter (usually included with Python)

### Run It

```bash
python main.py
```

# Controls

- Modes: Wall / Start / End – click to place

## Buttons:

- Wall: Toggle walls on the grid
- Start: Set the start point
- End: Set the end point
- Clear Grid: Reset everything
- Reset Search: Keep walls/start/end but clear visited path
- Run Flood Fill: Start the visualization
- Speed: Use the slider to adjust animation delay

## Concepts Used

- **Breadth-First Search (BFS)**
- **Graph traversal on grids**
- **Tkinter GUI programming**
- **Event-driven programming in Python**

## Future Improvements

- Add more algorithms (e.g., **DFS**, **A\***)
- Save/load maze layouts
- Support for diagonal movement
- Export path statistics
