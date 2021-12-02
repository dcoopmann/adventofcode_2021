import submarine

example_depths=submarine.import_measurement("test_sonar_measurements.txt")

def test_sonar_sweep():
    assert submarine.sonar_sweep(example_depths) == 5

def test_pytest():
    assert True

def test_navigation():
    assert submarine.calculate_navigation(submarine.import_commands("test_navigation_commands.txt") ) == 150