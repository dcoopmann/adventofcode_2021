import sonar

example_depths=sonar.import_measurement("test_measurements.txt")

def test_sonar_sweep():
    assert sonar.sonar_sweep(example_depths) == 5

def test_pytest():
    assert True