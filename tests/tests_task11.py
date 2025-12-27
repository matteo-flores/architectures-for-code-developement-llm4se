class TestTask11:
  """Test Suite for HumanEval/4 - mean_absolute_deviation"""

  def __init__(self, mean_absolute_deviation):
    self.fun = mean_absolute_deviation

  def get_benchmark_input(self):
    return ([1.0, 2.0, 3.0, 4.0],)

  def execute_tests(self):
    tests_passed = 0
    test_methods = [method for method in dir(self) if method.startswith('test_')]
    total_tests = len(test_methods)
    
    for method_name in test_methods:
      method = getattr(self, method_name)
      try:
        method()
        tests_passed += 1
      except Exception as e:
        print(f"[DEBUG]: Task 11 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_cases(self):
    assert abs(self.fun([1.0, 2.0, 3.0]) - 2.0/3.0) < 1e-6
    assert abs(self.fun([1.0, 2.0, 3.0, 4.0]) - 1.0) < 1e-6

  def test_02_five_elements(self):
    assert abs(self.fun([1.0, 2.0, 3.0, 4.0, 5.0]) - 6.0/5.0) < 1e-6

  def test_03_single_element(self):
    assert abs(self.fun([5.0]) - 0.0) < 1e-6

  def test_04_identical_elements(self):
    assert abs(self.fun([3.0, 3.0, 3.0, 3.0]) - 0.0) < 1e-6

  def test_05_negative_numbers(self):
    result = self.fun([-1.0, -2.0, -3.0])
    assert abs(result - 2.0/3.0) < 1e-6

  def test_06_mixed_positive_negative(self):
    result = self.fun([-2.0, 0.0, 2.0])
    expected = (2.0 + 0.0 + 2.0) / 3.0
    assert abs(result - expected) < 1e-6
