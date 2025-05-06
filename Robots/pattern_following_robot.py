from Robots.base_robot import BaseRobot, Feature, Action

class PatternFollowingRobot(BaseRobot):
    def __init__(self, name='Pattern Bot'):
        super().__init__(name)
        self.direction = 1  # 1 means moving right, -1 means moving left
        self.target_x, self.target_y = 0, 0  # Start at the top-left of the grid

    def update_target_position(self):
        # Move horizontally within the row based on direction
        if 0 <= self.target_x + self.direction < 10:
            self.target_x += self.direction
        else:
            # If we reach the end of a row, move down one row and switch direction
            if self.target_y < 9:  # Ensure we stay within grid bounds
                self.target_y += 1
                self.direction *= -1  # Flip direction for zigzag

    def choose_action(self):
        # Sense the surroundings and set data for centre, north, east, south, and west squares
        self.sense_environment()

        # Step 1: Pick up a can if there is one in the current square
        if self.sensory_data.centre_square == Feature.can:
            return Action.pick_up_can

        # Step 2: Look for nearby cans and prioritize moving towards them
        if self.sensory_data.north_square == Feature.can:
            return Action.move_north
        elif self.sensory_data.south_square == Feature.can:
            return Action.move_south
        elif self.sensory_data.east_square == Feature.can:
            return Action.move_east
        elif self.sensory_data.west_square == Feature.can:
            return Action.move_west

        # Step 3: Follow the search grid pattern to reach the target position
        if self.x < self.target_x:
            action = Action.move_east
        elif self.x > self.target_x:
            action = Action.move_west
        elif self.y < self.target_y:
            action = Action.move_south
        elif self.y > self.target_y:
            action = Action.move_north
        else:
            # Update target to the next position in the pattern
            self.update_target_position()
            action = Action.do_nothing  # Momentary pause once target is reached

        # Step 4: Check for walls before moving in the selected direction
        if (action == Action.move_north and self.sensory_data.north_square == Feature.wall) or \
           (action == Action.move_south and self.sensory_data.south_square == Feature.wall) or \
           (action == Action.move_east and self.sensory_data.east_square == Feature.wall) or \
           (action == Action.move_west and self.sensory_data.west_square == Feature.wall):
            # Move down one row to avoid the wall, if possible
            if self.target_y < 9:
                self.target_y += 1
            action = Action.move_south  # Move down if we encounter a wall

        return action
