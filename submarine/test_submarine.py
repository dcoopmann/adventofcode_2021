import sonar

example_depths=sonar.import_measurement("test_measurements.txt")

def test_sonar_sweep():
    assert sonar.sonar_sweep(example_depths) == 7

def test_pytest():
    assert True