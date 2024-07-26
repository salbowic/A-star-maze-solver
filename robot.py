class Robot:
    def __init__(self, robot_info):
        self.position = robot_info['position']  # (x, y) coordinates
        self.orientation = robot_info['orientation']  # N, S, W, E

    def move_forward(self):
        if self.orientation == 'N':
            self.position = (self.position[0], self.position[1] - 1)
        elif self.orientation == 'S':
            self.position = (self.position[0], self.position[1] + 1)
        elif self.orientation == 'W':
            self.position = (self.position[0] - 1, self.position[1])
        elif self.orientation == 'E':
            self.position = (self.position[0] + 1, self.position[1])

    def move_backward(self):
        if self.orientation == 'N':
            self.position = (self.position[0], self.position[1] + 1)
        elif self.orientation == 'S':
            self.position = (self.position[0], self.position[1] - 1)
        elif self.orientation == 'W':
            self.position = (self.position[0] + 1, self.position[1])
        elif self.orientation == 'E':
            self.position = (self.position[0] - 1, self.position[1])

    def turn_right(self):
        directions = ['N', 'E', 'S', 'W']
        idx = directions.index(self.orientation)
        self.orientation = directions[(idx + 1) % 4]

    def turn_left(self):
        directions = ['N', 'E', 'S', 'W']
        idx = directions.index(self.orientation)
        self.orientation = directions[(idx - 1) % 4]

    def efficient_turn(self, next_position):
        required_orientation = self.get_required_orientation(next_position)
        while self.orientation != required_orientation:
            directions = ['N', 'E', 'S', 'W']
            current_idx = directions.index(self.orientation)
            target_idx = directions.index(required_orientation)

            # Calculate the difference in both directions
            right_turns = (target_idx - current_idx) % 4
            left_turns = (current_idx - target_idx) % 4

            # Turn in the direction of the shorter rotation
            if right_turns <= left_turns:
                for _ in range(right_turns):
                    self.turn_right()
            else:
                for _ in range(left_turns):
                    self.turn_left()

    def teleport(self, next_position):
        self.position = next_position

    def get_required_orientation(self, next_position):
        current_x, current_y = self.position
        next_x, next_y = next_position
        # Determine the relative direction of the next move
        if next_x == current_x + 1:  # Move East
            required_orientation = 'E'
        elif next_x == current_x - 1:  # Move West
            required_orientation = 'W'
        elif next_y == current_y + 1:  # Move South
            required_orientation = 'S'
        elif next_y == current_y - 1:  # Move North
            required_orientation = 'N'
        else:
            raise ValueError("Invalid next position")
        
        return required_orientation

    def is_move_teleport(self, next_position):
        current_x, current_y = self.position
        next_x, next_y = next_position
        if abs(next_x - current_x) + abs(next_y - current_y) != 1:
            return True

    def move_robot_to_next_position(self, next_position, maze):
        # Check if next position is adjacent
        if self.is_move_teleport(next_position):
            # Implement logic to move back
            self.teleport(next_position)
            
        else:
            self.efficient_turn(next_position)
            # Move forward to the next position
            self.move_forward()
            maze.total_moves += 1

    def __repr__(self):
        return f"Robot(position={self.position}, orientation={self.orientation})"
