import time
from collections import deque

class FloodFillAlgorithm:
    def __init__(self, grid, start, end, algorithm, speed_callback=None, update_callback=None):
        self.grid = grid
        self.start = start
        self.end = end
        self.speed_callback = speed_callback  # Function to get speed
        self.update_callback = update_callback  # Function to update UI
        self.algorithm = algorithm
    
    def search(self):
        if self.algorithm == 'dfs':
            return self.dfs()
        else:
            return self.bfs()

    def bfs(self):
        if not self.start or not self.end:
            return False

        width = len(self.grid[0])
        height = len(self.grid)
        queue = deque([(self.start[0], self.start[1], [])])
        visited = set()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # down, right, up, left

        while queue:
            x, y, path = queue.popleft()

            if (x, y) in visited:
                continue

            visited.add((x, y))

            # Mark as visited (except start and end)
            if (x, y) != self.start and (x, y) != self.end:
                self.grid[y][x] = 4
                if self.update_callback:
                    self.update_callback()
                if self.speed_callback:
                    time.sleep(self.speed_callback())

            # Check if we reached the end
            if (x, y) == self.end:
                # Draw the path
                for px, py in path:
                    if (px, py) != self.start and (px, py) != self.end:
                        self.grid[py][px] = 5
                if self.update_callback:
                    self.update_callback()
                return True

            # Explore neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if (0 <= nx < width and 0 <= ny < height and
                    (nx, ny) not in visited and self.grid[ny][nx] != 1):

                    new_path = path + [(x, y)]
                    queue.append((nx, ny, new_path))

        return False
    
    def dfs(self):
        if not self.start or not self.end:
            return False

        width = len(self.grid[0])
        height = len(self.grid)
        stack = [(self.start[0], self.start[1], [])]
        visited = set()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # down, right, up, left

        while stack:
            x, y, path = stack.pop()

            if (x, y) in visited:
                continue

            visited.add((x, y))

            # Mark as visited (except start and end)
            if (x, y) != self.start and (x, y) != self.end:
                self.grid[y][x] = 4
                if self.update_callback:
                    self.update_callback()
                if self.speed_callback:
                    time.sleep(self.speed_callback())

            # Check if we reached the end
            if (x, y) == self.end:
                # Draw the path
                for px, py in path:
                    if (px, py) != self.start and (px, py) != self.end:
                        self.grid[py][px] = 5
                if self.update_callback:
                    self.update_callback()
                return True

            # Explore neighbors (reverse order for DFS to maintain consistent direction priority)
            for dx, dy in reversed(directions):
                nx, ny = x + dx, y + dy

                if (0 <= nx < width and 0 <= ny < height and
                    (nx, ny) not in visited and self.grid[ny][nx] != 1):

                    new_path = path + [(x, y)]
                    stack.append((nx, ny, new_path))

        return False