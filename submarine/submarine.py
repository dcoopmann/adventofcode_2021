import typing
import logging

def import_measurement(file) -> typing.List[int]:
    measurement = []
    with open(file) as f:
        for line in f:
            measurement.append(int(line))
    
    return measurement

def import_commands(file) -> list:
    commands = []
    with open(file) as f:
        for line in f:
            commands.append(line.split())
    return commands

def sonar_sweep(depth_measurement:typing.List[int])-> int:
    depth_increased_times = 0
    current_depth_window = depth_measurement[0] + depth_measurement[1] + depth_measurement[2]
    logging.debug(f"initial depth_measurement: {depth_measurement}")
    logging.debug(f"initial current_depth_window: {current_depth_window}")
    
    depth_measurement.pop(0) # Remove since only relevant for first measurement window
    logging.debug(f"after pop() depth_measurement: {depth_measurement}")
    
    for measurement in enumerate(depth_measurement):
        logging.debug(f"measurement: {measurement}")
        try:
            window = depth_measurement[measurement[0]] + depth_measurement[measurement[0] + 1] + depth_measurement[measurement[0] + 2]
            logging.debug(f"window: {window}")
            if current_depth_window < window:
                depth_increased_times += 1
            current_depth_window = window
        except IndexError:
            logging.debug("ignore sliding windows with not enough measurements")

    return depth_increased_times

def calculate_navigation(commands: list) -> int:
    x = 0
    y = 0

    for command in commands:
        if command[0] == "up":
            y -= int(command[1])
        elif command[0] == "down":
            y += int(command[1])
        elif command[0] == "forward":
            x += int(command[1])

    return (x*y)

if __name__ == "__main__":
    print(calculate_navigation(import_commands("navigation_commands.txt")))