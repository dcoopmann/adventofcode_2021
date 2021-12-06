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
            # report.append(list(line))
            report.append([x for x in list(line) if x != "\n"])
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

def preprocess_diagnostics(report : typing.List[list[int]], balanced_bit: str):
    # balanced_bit: if 0 and 1 are equally distributed in row set bit to balanced_bit
    
    gamma_rate = b""
    epsilon_rate = b""

    print(f"report: {report}")

    for i in range(0,len(report[0])):
        gamma_bit = 0
        for line in report:
            if line[i] == "1":
                gamma_bit += 1
            else:
                gamma_bit -= 1
        
        print(f"gamma bit: {gamma_bit}")
        if gamma_bit >= 0:
            gamma_rate += b"1"
        # elif gamma_bit == 0:
        #     gamma_rate += balanced_bit
        else:
            gamma_rate += b"0"
        print(f"gamma_rate: {gamma_rate}")
    epsilon_rate = gamma_rate.replace(b"1",b"2").replace(b"0",b"1").replace(b"2",b"0")

    print(f"gamma_rate, epsilon_rate: {gamma_rate, epsilon_rate}") 
    return [gamma_rate, epsilon_rate]

def diag_power_consumption(power_data: list):
    pd = preprocess_diagnostics(power_data, b"1")
    return int(pd[0], 2) * int(pd[1], 2)

#TODO: Test ist Correct, but false Positive since puzzle output is not right atm
def diag_live_support(life_data: list):
    # oxygen = b""
    # co_two = b""

    # most common bit for Oxygen
    oxy_data = get_life_support_data(life_data, True, b"1")
    # least common bit for CO2
    co_two_data = get_life_support_data(life_data, False, b"0")
    oxygen = fill_binary_life_support_values(oxy_data)
    co_two = fill_binary_life_support_values(co_two_data)
    
    return int(oxygen, 2) * int(co_two,2)
    # return co_two_data

def get_life_support_data(life_data: list, most_common: bool, eq_bit: str) -> list:
    if most_common:
        mc_int = 0
    else: 
        mc_int = 1
    
    data = life_data
    i = 0
    # for i in range(len(life_data[0])):
    while len(data) > 1:
        print(f"-------------------i:{i}--------------------")
        
        tmp=[]
        
        bit_criteria = list(preprocess_diagnostics(data, eq_bit)[mc_int].decode())
        # print(f"bit criteria, i: {bit_criteria}, {i}")
        print(f"bit_criteria: {bit_criteria}")
        # for i in range(0,len(bit_criteria)):
        for d in data:
            # print(f"data: {d}")
            if d[i] == bit_criteria[i]:
                print(f"match for bit_c[i] {bit_criteria[i]} in {d} at index: {i}")
                tmp.append(d)
        i+=1        
        #     if d[i] == bit_criteria[i]:
        #         print(f"d[i]:{d[i]}, bit_crit[i]:{bit_criteria[i]}")
                # tmp.append(d)

        print(f"data before tmp: {data}")
        print(f"tmp: {tmp}")
        data = tmp
        print(f"data after tmp: {data}")

        # if len(data) == 1:
        #     break


    return data[0][0:5]

def fill_binary_life_support_values(value):
    s = b""
    for v in value:
        if v == "0":
            s += b"0"
        if v == "1":
            s += b"1"
    return s


    


if __name__ == "__main__":
    # print(calculate_navigation(import_commands("navigation_commands.txt")))
    print(diag_live_support(import_diag_report("diag_report.txt")))