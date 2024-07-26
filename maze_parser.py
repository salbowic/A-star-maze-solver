import pygame
from cell import Cell

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255,165,0)

class Maze:
    def __init__(self, maze_file_path):
        self.size = self._get_maze_size(maze_file_path)
        self._create_maze_grid(maze_file_path)
        self.robot_info, self.starting_position = self._get_info(maze_file_path)
        self.reward_squares = self._get_rewards_squares()
        self.total_search_cost = 0
        self.total_moves = 0
        self.wait_time = 50
        self.best_path_found = False
    
    def _create_pygame_screen(self, margin_width, cell_size):
        self.cell_size = cell_size
        width = self.size[0] * self.cell_size + margin_width
        height = self.size[1] * self.cell_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Maze")

    def _get_vertical_walls(self, maze_def_lines):
        vertical_walls_lines = maze_def_lines[2:2 + self.size[1]]
        for row, line in enumerate(vertical_walls_lines):
            walls = line.strip().split()
            for col, wall in enumerate(walls):
                if wall == '1':
                    if col < self.size[0]:
                        self.maze_grid[row][col].walls['E'] = 1
                        self.maze_grid[row][col + 1].walls['W'] = 1
    
    def _get_horizontal_walls(self, maze_def_lines):
        horizontal_walls_lines = maze_def_lines[2 + self.size[1]:]
        for row, line in enumerate(horizontal_walls_lines):
            walls = line.strip().split()
            for col, wall in enumerate(walls):
                if wall == '1':
                    if row < self.size[1]:
                        self.maze_grid[row][col].walls['S'] = 1
                        self.maze_grid[row + 1][col].walls['N'] = 1

    def _add_border_walls(self):
        rows = self.size[1]
        cols = self.size[0]
        for i in range(rows):
            self.maze_grid[i][0].walls['W'] = 1  # Add west wall to the first column
            self.maze_grid[i][cols - 1].walls['E'] = 1  # Add east wall to the last column
        for j in range(cols):
            self.maze_grid[0][j].walls['N'] = 1  # Add north wall to the first row
            self.maze_grid[rows - 1][j].walls['S'] = 1  # Add south wall to the last row

    def _get_rewards_squares(self):
        mid_x, mid_y = self.size[0] // 2, self.size[1] // 2
        if self.size[0] % 2 == 0 and self.size[1] % 2 == 0:
            reward_squares = [
                (mid_x, mid_y), (mid_x - 1, mid_y), (mid_x, mid_y - 1), (mid_x - 1, mid_y - 1)
            ]
        else:
            reward_squares = [
                (mid_x, mid_y), (mid_x - 1, mid_y), (mid_x, mid_y - 1), (mid_x - 1, mid_y - 1)
            ]
        return reward_squares

    def _get_maze_lines(self, maze_file_path):
        with open(maze_file_path, 'r') as file:
            maze_def_lines = file.read().splitlines()
        # Filter out any empty lines
        maze_def_lines = [line for line in maze_def_lines if line.strip() != '']
        return maze_def_lines

    def _get_maze_size(self, maze_file_path):
        maze_def_lines = self._get_maze_lines(maze_file_path)
        # Read the size of the maze
        size_line = maze_def_lines[0].strip().split()
        size = (int(size_line[0]), int(size_line[1]))
        return size

    def _get_info(self, maze_file_path):
        maze_def_lines = self._get_maze_lines(maze_file_path)
        # Read the robot's starting position and orientation
        robot_line = maze_def_lines[1].strip().split()
        robot_info = {'position': (int(robot_line[0]), int(robot_line[1])), 'orientation': robot_line[2]}
        starting_position = robot_info['position']

        return robot_info, starting_position

    def _create_maze_grid(self, maze_file_path):
        maze_def_lines = self._get_maze_lines(maze_file_path)
        # Initialize the maze grid with empty lists
        self.maze_grid = [[Cell() for _ in range(self.size[0])] for _ in range(self.size[1])]

        #Add border walls to maze grid
        self._add_border_walls()

        # Parse vertical walls (size[1] rows)
        self._get_vertical_walls(maze_def_lines)

        # Parse horizontal walls (size[0] rows)
        self._get_horizontal_walls(maze_def_lines)

    def _display_start_cell(self, color):
        x, y = self.starting_position
        pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def _display_maze_walls(self):
        line_width = 3
        for y in range(len(self.maze_grid)):
            for x in range(len(self.maze_grid[y])):
                cell = self.maze_grid[y][x]
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

                # Draw the walls for the cell
                if cell.walls['N']:
                    pygame.draw.line(self.screen, BLACK, rect.topleft, rect.topright, line_width)
                if cell.walls['S']:
                    pygame.draw.line(self.screen, BLACK, rect.bottomleft, rect.bottomright, line_width)
                if cell.walls['E']:
                    pygame.draw.line(self.screen, BLACK, rect.topright, rect.bottomright, line_width)
                if cell.walls['W']:
                    pygame.draw.line(self.screen, BLACK, rect.topleft, rect.bottomleft, line_width)

    def _display_robot(self):
        # Define the path to the robot images
        orientation_to_image = {
            'N': 'robot_N.png',
            'S': 'robot_S.png',
            'W': 'robot_W.png',
            'E': 'robot_E.png'
        }

        # Load the image based on the robot's orientation
        orientation = self.robot_info['orientation']
        robot_image_path = f'images/{orientation_to_image[orientation]}'
        robot_image = pygame.image.load(robot_image_path)
        robot_image = pygame.transform.scale(robot_image, (self.cell_size, self.cell_size))  # Scale the image to fit the cell

        # Get the robot's position on the grid
        robot_x, robot_y = self.robot_info['position']

        # Blit the image onto the screen at the robot's position
        self.screen.blit(robot_image, (robot_x * self.cell_size, robot_y * self.cell_size))

    def _display_reward_squares(self, color):
        for (x, y) in self.reward_squares:
            pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def _display_path_cell(self, position, color):
        x, y = position
        color = GRAY if position == self.starting_position else color
        pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def _display_final_goal(self, final_goal):
        reward_image_path = 'images/reward.png'
        reward_image = pygame.image.load(reward_image_path)
        reward_image = pygame.transform.scale(reward_image, (self.cell_size, self.cell_size))
        self.screen.blit(reward_image, (final_goal[0] * self.cell_size, final_goal[1] * self.cell_size))
        
    def _display_statistics(self):
        font = pygame.font.Font('fonts/Minecraftia-Regular.ttf', 20)

        # Position for the first line of text
        text_x = self.size[0] * self.cell_size + 20
        text_y_start = 20
        line_height = 25

        # Render and display total search cost
        search_cost_text = font.render(f'Total Cost: {self.total_search_cost}', True, BLACK)
        self.screen.blit(search_cost_text, (text_x, text_y_start))

        # Render and display total moves
        moves_text = font.render(f'Total Moves: {self.total_moves}', True, BLACK)
        self.screen.blit(moves_text, (text_x, text_y_start + line_height))

        if self.n_of_visited_cells:
            visited_text = font.render(f'Cells Visited: {self.n_of_visited_cells}', True, BLACK)
            self.screen.blit(visited_text, (text_x, text_y_start + 2 * line_height))

        # Render and display the cost of the best path
        if self.best_path_found:
            best_path_cost_text = font.render(f'Best Path Cost: {self.best_path_cost}', True, BLACK)
            self.screen.blit(best_path_cost_text, (text_x, text_y_start + 3 * line_height))
    
    def display_legend(self, show_final=False):
        font = pygame.font.Font('fonts/Minecraftia-Regular.ttf', 20)
        legend_items = [
            ("gray square", GRAY, "Start"),
            ("red square", RED, "Goal"),
            ("yellow square", YELLOW, "Visited Squares"),
            ("orange square", ORANGE, "Discovered Squares")
        ]
        if show_final:
            legend_items.append(("green square", GREEN, "Found solution"))

        start_x = self.size[0] * self.cell_size + 20 
        start_y = self.size[1] * self.cell_size - 140
        square_size = 20
        padding = 5
        text_padding = 10

        for i, (key, color, text) in enumerate(legend_items):
            square_y = start_y + i * (square_size + padding)
            # Draw the color square
            pygame.draw.rect(self.screen, color, (start_x, square_y, square_size, square_size))
            # Draw the text label
            label = font.render(text, True, BLACK)
            self.screen.blit(label, (start_x + square_size + text_padding, square_y))

    def display_maze(self, visited_cells=None, discovered_cells=None, path=None, final_goal=None, show_final=False):
        # Initialize Pygame
        pygame.init()
        # Show final solution (if it's found)
        if show_final:
            self.best_path_found = True
            self.screen.fill(WHITE)

            if visited_cells:
                self.n_of_visited_cells = len(visited_cells)
                for position in visited_cells:
                    self._display_path_cell(position, YELLOW)

            if discovered_cells:
                for position in discovered_cells:
                    self._display_path_cell(position, ORANGE)

            if path:
                for position in path:
                    self._display_path_cell(position, GREEN)
            
            self._display_reward_squares(RED)

            if final_goal:
                self._display_final_goal(final_goal)

            self._display_maze_walls()
            # Display statistics outside the maze area
            self._display_statistics()

            self.display_legend(True)

            # Update the display
            pygame.display.flip()

            # Save the screen as an image file
            pygame.image.save(self.screen, "final_maze_solution.png")

            # Keep the window open until it is closed by the user
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            pygame.quit()

        else:
            # Fill the background
            self.screen.fill(WHITE)
            
            self._display_start_cell(GRAY)

            if visited_cells:
                self.n_of_visited_cells = len(visited_cells)
                for position in visited_cells:
                    self._display_path_cell(position, YELLOW)
            
            if discovered_cells:
                for position in discovered_cells:
                    self._display_path_cell(position, ORANGE)

            # Draw the path
            if path:
                for position in path:
                    self._display_path_cell(position, GREEN)

            # Draw the reward squares
            self._display_reward_squares(RED)
            
            self._display_maze_walls()
            
            # Draw the robot
            self._display_robot()

            # Display the current cost
            font = pygame.font.Font('fonts/Minecraftia-Regular.ttf', 20)
            cost_text = font.render(f'Cost: {self.total_search_cost}', True, BLACK)
            self.screen.blit(cost_text, (self.size[0] * self.cell_size + 10, 10))  # Position the text on the screen

            # Display the number of moves
            moves_text = font.render(f'Moves: {self.total_moves}', True, BLACK)
            self.screen.blit(moves_text, (self.size[0] * self.cell_size + 10, 60))  # Adjust position as needed

            self.display_legend()

            # Update the display
            pygame.display.flip()
            pygame.time.wait(self.wait_time)

    pygame.quit()
                
