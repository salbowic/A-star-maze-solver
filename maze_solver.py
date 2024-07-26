from maze_parser import Maze
import heapq
from robot import Robot

class MazeSolver(Maze):
    def __init__(self, maze_file_path):
        super().__init__(maze_file_path)
        self.final_goal = None

    def heuristic(self, a, b):
        # Manhattan distance on a square grid ** 2
        return (min(abs(a[0] - bx[0]) + abs(a[1] - bx[1]) for bx in b))**2

    def a_star_search(self, display = True):

        if display == True:
            self._create_pygame_screen(320, 40)

        robot = Robot(self.robot_info)
        start = self.starting_position
        goals = set(self.reward_squares)

        open_set = []
        heapq.heappush(open_set, (0, start))  # (priority, position)

        came_from = {start: None}
        cost_so_far = {start: 0}
        visited_cells = set()
        discovered_cells = set([self.starting_position]) 

        while open_set:
            current = heapq.heappop(open_set)[1]
            robot.move_robot_to_next_position(current, self)
            self.robot_info = {'position': (int(robot.position[0]), int(robot.position[1])), 'orientation': robot.orientation}
            
            visited_cells.add(current)
            discovered_cells.discard(current)
            
            if display:
                self.display_maze(visited_cells=visited_cells, discovered_cells=discovered_cells)
            
            if current in goals:
                self.final_goal = current
                path = self.reconstruct_path(came_from, start, self.final_goal)
                self.best_path_cost = len(path) - 1
                self._display_final_path_in_console(path, cost_so_far)

                if display:
                    self.display_maze(visited_cells=visited_cells, discovered_cells=discovered_cells, path=path, final_goal=self.final_goal, show_final=True)
                break
                    
            for next_cell in self.get_neighbors(current):
                if next_cell not in visited_cells and next_cell not in discovered_cells:
                    discovered_cells.add(next_cell)
                    
                new_cost = cost_so_far[current] + self.move_cost(current, next_cell)
                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    priority = new_cost + self.heuristic(next_cell, goals)
                    heapq.heappush(open_set, (priority, next_cell))
                    came_from[next_cell] = current
                    
                
                if next_cell != robot.position:
                    robot.move_robot_to_next_position(next_cell, self)
                    self.total_search_cost += 1
            
    def move_cost(self, current, next):
        return abs(next[0] - current[0]) + abs(next[1] - current[1])

    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # N, S, W, E
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size[0] and 0 <= ny < self.size[1]:
                if not self.is_wall_between(position, (nx, ny)):
                    neighbors.append((nx, ny))
        return neighbors
    
    def is_wall_between(self, pos1, pos2):
        cell = self.maze_grid[pos1[1]][pos1[0]]
        if pos1[0] == pos2[0] and pos1[1] == pos2[1] - 1:  # South
            return cell.walls['S']
        elif pos1[0] == pos2[0] and pos1[1] == pos2[1] + 1:  # North
            return cell.walls['N']
        elif pos1[0] == pos2[0] - 1 and pos1[1] == pos2[1]:  # East
            return cell.walls['E']
        elif pos1[0] == pos2[0] + 1 and pos1[1] == pos2[1]:  # West
            return cell.walls['W']
        return True  # Return True if not adjacent

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()  # reverse path to start to goal
        return path

    def _display_final_path_in_console(self, path, closed_set):
        path_str = ' -> '.join(f"({x}, {y})" for x, y in path)
        path_cost = len(path) - 1
        print("Final Path:", path_str)
        print("Final Path Cost (moves):", path_cost)
        print("Cost to find final path:", self.total_search_cost)
        print("Number of moves:", self.total_moves) 
        print("Number of visited cells:", len(closed_set))
