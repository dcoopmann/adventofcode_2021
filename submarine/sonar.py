import typing

def import_measurement(file) -> typing.List[int]:
    measurement = []
    with open(file) as f:
        for line in f:
            measurement.append(int(line))
    
    return measurement

def sonar_sweep(depth_measurement:typing.List[int])-> int:
    depth_increased_times = 0
    current_depth = depth_measurement.pop(0)

    for measurement in depth_measurement:
        if current_depth < measurement:
            depth_increased_times += 1
        current_depth = measurement
    
    return depth_increased_times

if __name__ == "__main__":
    print(import_measurement("sonar_measurement.txt"))