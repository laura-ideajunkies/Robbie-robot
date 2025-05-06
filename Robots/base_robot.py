from random import choice

from action import Action
from environment import Environment
from sensory_data import SensoryData, Feature


class BaseRobot:
    def __init__(self, name=''):
        self.x = 0
        self.y = 0
        self.name = name
        self.actions = [Action.pick_up_can, Action.move_north, Action.move_south, Action.move_west,
                        Action.move_east, Action.move_random, Action.do_nothing]
        self.score = 0
        self.sensory_data = SensoryData()
        self.situation_number = 0
        self.environment = None

    def set_environment(self, environment):
        self.environment = environment

    def choose_action(self):
        # Choose an action at random
        return choice(self.actions)

    def sense_environment(self):
        sensor_string = ''
        for (x, y) in [(self.x, self.y - 1),
                       (self.x - 1, self.y),
                       (self.x, self.y),
                       (self.x + 1, self.y),
                       (self.x, self.y + 1)]:
            if x == -1 or x == Environment.LENGTH or y == -1 or y == Environment.LENGTH:
                symbol = '2'
            else:
                symbol = str(self.environment.grid[x][y])
            sensor_string += symbol

        self.situation_number = 0
        for i in range(0, 5):
            self.situation_number += int(sensor_string[i]) * 3 ** i

        self.sensory_data.north_square = Feature.wall if sensor_string[0] == '2' \
            else Feature.can if sensor_string[0] == '1' else Feature.empty
        self.sensory_data.west_square = Feature.wall if sensor_string[1] == '2' \
            else Feature.can if sensor_string[1] == '1' else Feature.empty
        self.sensory_data.centre_square = Feature.wall if sensor_string[2] == '2' \
            else Feature.can if sensor_string[2] == '1' else Feature.empty
        self.sensory_data.east_square = Feature.wall if sensor_string[3] == '2' \
            else Feature.can if sensor_string[3] == '1' else Feature.empty
        self.sensory_data.south_square = Feature.wall if sensor_string[4] == '2' \
            else Feature.can if sensor_string[4] == '1' else Feature.empty

    def calculate_situation_number(self):
        self.situation_number = 0
        for (x, y, multiplier) in [(self.x,     self.y - 1,  1),
                                   (self.x - 1, self.y,      3),
                                   (self.x,     self.y,      9),
                                   (self.x + 1, self.y,     27),
                                   (self.x,     self.y + 1, 81)]:
            if y == -1 or y == Environment.LENGTH or x == -1 or x == Environment.LENGTH:
                self.situation_number += 2 * multiplier
            else:
                self.situation_number += self.environment.grid[x][y] * multiplier
