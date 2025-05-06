from enum import Enum

Feature = Enum('Feature', 'wall can empty')


class SensoryData:
    def __init__(self):
        self.north_square = None
        self.south_square = None
        self.east_square = None
        self.west_square = None
        self.centre_square = None

    def display(self):
        print([['', self.north_square, ''],
               [self.west_square, self.centre_square, self.east_square],
               ['', self.south_square, '']])
