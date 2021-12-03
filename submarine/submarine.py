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

def import_diag_report(file) -> typing.List[list[int]]:
    report = []
    with open(file) as f:
        for line in f:
            report.append(list(line))
    return report

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
    aim = 0

    for command in commands:
        if command[0] == "up":
            aim -= int(command[1])
        elif command[0] == "down":
            aim += int(command[1])
        elif command[0] == "forward":
            x += int(command[1])
            y += int(command[1]) * aim

    return (x*y)

def preprocess_diagnostics(report : typing.List[list[int]]):
    gamma_rate = b""
    epsilon_rate = b""

    bitlength = len(report[0]) - 1
    
    for i in range(0,bitlength):
        gamma_bit = 0
        for line in report:
            if line[i] == "1":
                gamma_bit += 1
            else:
                gamma_bit -= 1
        
        if gamma_bit >= 1:
            gamma_rate += b"1"
        else:
            gamma_rate += b"0"

    # decimal_gamma = int(gamma_rate, 2)
    epsilon_rate = gamma_rate.replace(b"1",b"2").replace(b"0",b"1").replace(b"2",b"0")
    # decimal_epsilon = int(epsilon_rate, 2)
    
    return [gamma_rate, epsilon_rate]

def diag_power_consumption(power_data):
    pd = preprocess_diagnostics(power_data)
    return int(pd[0], 2) * int(pd[1], 2)



if __name__ == "__main__":
    # print(calculate_navigation(import_commands("navigation_commands.txt")))
    print(diag_power_consumption(import_diag_report("diag_report.txt")))