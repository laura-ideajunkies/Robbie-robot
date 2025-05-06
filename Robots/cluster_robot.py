from Robots.can_following_robot import CanFollowingRobot, Feature, Action
from random import choice

class ClusterRobot(CanFollowingRobot):
    def __init__(self, name='Cluster Bot'):
        super().__init__(name)
        self.cluster_count = 0  # Tracks consecutive cans picked up
        self.spiral_active = False  # Whether the spiral search is active
        self.spiral_radius = 1  # Current radius of the spiral
        self.spiral_directions = ["right", "down", "left", "up"]  # Spiral directions in order
        self.spiral_direction_index = 0  # Index in spiral_directions

    def reset_spiral(self):
        """Resets spiral search parameters when starting a new cluster or resuming regular search."""
        self.spiral_active = False
        self.spiral_radius = 1
        self.spiral_direction_index = 0

    def activate_spiral(self):
        """Activates spiral search from the current location."""
        self.spiral_active = True
        self.spiral_radius = 1
        self.spiral_direction_index = 0

    def update_spiral_position(self):
        """Updates the robot’s target position based on sensing for walls in a spiral pattern."""
        # Determine the current direction
        direction = self.spiral_directions[self.spiral_direction_index]

        # Check for walls in the current direction
        if (direction == "right" and self.sensory_data.east_square == Feature.wall) or \
           (direction == "down" and self.sensory_data.south_square == Feature.wall) or \
           (direction == "left" and self.sensory_data.west_square == Feature.wall) or \
           (direction == "up" and self.sensory_data.north_square == Feature.wall):
            # If a wall is detected, turn to the next direction in the spiral
            self.spiral_direction_index = (self.spiral_direction_index + 1) % 4
            direction = self.spiral_directions[self.spiral_direction_index]

        # Set target position based on the current direction in the spiral
        if direction == "right":
            self.target_x = self.x + 1
            self.target_y = self.y
        elif direction == "down":
            self.target_x = self.x
            self.target_y = self.y + 1
        elif direction == "left":
            self.target_x = self.x - 1
            self.target_y = self.y
        elif direction == "up":
            self.target_x = self.x
            self.target_y = self.y - 1

    def choose_action(self):
        # Sense surroundings to determine if there are any cans
        self.sense_environment()

        # Step 1: Pick up a can if there is one in the current square, increment cluster count
        if self.sensory_data.centre_square == Feature.can:
            self.cluster_count += 1
            if self.cluster_count >= 3:  # Start spiral search after picking up 3 consecutive cans
                self.activate_spiral()
            return Action.pick_up_can

        # Step 2: If spiral is active, execute the spiral search pattern
        if self.spiral_active:
            self.update_spiral_position()
            if self.x < self.target_x:
                action = Action.move_east
            elif self.x > self.target_x:
                action = Action.move_west
            elif self.y < self.target_y:
                action = Action.move_south
            elif self.y > self.target_y:
                action = Action.move_north
            else:
                # Complete one layer of the spiral, then expand the radius by 1
                self.spiral_radius += 1
                self.update_spiral_position()
                action = Action.do_nothing  # Pause momentarily once reaching target

            # Deactivate spiral if a can is found in the current square during spiral search
            if self.sensory_data.centre_square == Feature.can:
                self.reset_spiral()

            # If no cans are found after a few spiral layers, resume regular can-following
            if self.spiral_radius > 5:  # Adjust radius threshold as needed
                self.reset_spiral()
            return action

        # Step 3: Default can-following behavior from CanFollowingRobot
        action = super().choose_action()

        # Step 4: Reset cluster count and spiral if no can was picked up
        if action != Action.pick_up_can:
            self.cluster_count = 0
            self.reset_spiral()

        return action
