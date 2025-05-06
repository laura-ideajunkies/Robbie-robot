from Robots.smarter_sensing_robot import SmarterSensingRobot, Feature, Action
from random import choice


class CanFollowingRobot(SmarterSensingRobot):
    def choose_action(self):
        # Use the SmarterSensingRobot to get the default action.
        action = SmarterSensingRobot.choose_action(self)

        # Favour actions that walk towards a can if we can't pick one up right now.
        if action != Action.pick_up_can:
            replacement_actions = []
            if self.sensory_data.north_square == Feature.can:
                replacement_actions.append(Action.move_north)
            if self.sensory_data.east_square == Feature.can:
                replacement_actions.append(Action.move_east)
            if self.sensory_data.south_square == Feature.can:
                replacement_actions.append(Action.move_south)
            if self.sensory_data.west_square == Feature.can:
                replacement_actions.append(Action.move_west)
            if len(replacement_actions) > 0:
                action = choice(replacement_actions)

        return action
