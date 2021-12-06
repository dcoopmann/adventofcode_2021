import submarine

example_depths=submarine.import_measurement("test_sonar_measurements.txt")

def test_sonar_sweep():
    assert submarine.sonar_sweep(example_depths) == 5

def test_pytest():
    assert True

def test_navigation():
    assert submarine.calculate_navigation(submarine.import_commands("test_navigation_commands.txt") ) == 900

def test_power_diagnostics():
    assert submarine.diag_power_consumption(submarine.import_diag_report("test_diag_report.txt")) == 198

def test_diag_live_support():
    assert submarine.diag_live_support(submarine.import_diag_report("test_diag_report.txt")) == 230
