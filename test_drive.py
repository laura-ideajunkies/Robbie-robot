from environment import Environment
from Robots.experimental_robot import ExperimentalRobot as Robot


NUMBER_OF_ACTIONS = 200
NUMBER_OF_TRIALS = 1

test_robot = Robot('Robot under test')
environment = Environment()

total_score = 0

for _ in range(NUMBER_OF_TRIALS):
    environment.randomise()
    test_robot.set_environment(environment)
    environment.set_robot(test_robot)
    environment.display(test_robot.x, test_robot.y)
    for i in range(NUMBER_OF_ACTIONS):
        action = test_robot.choose_action()
        current_score = test_robot.score
        environment.perform_action(action)
        updated_score = test_robot.score
        environment.display(test_robot.x, test_robot.y)
        print(action, test_robot.score, i)
    print(test_robot.score)
    total_score += test_robot.score

average_score = total_score / NUMBER_OF_TRIALS

print('Average score:', average_score)
