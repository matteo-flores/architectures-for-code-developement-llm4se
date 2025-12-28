class TestTask8:
  """Test Suite for CodeNet/p03260 - is_odd_product"""

  def __init__(self, is_odd_product):
    self.fun = is_odd_product

  def get_benchmark_input(self):
    return (3, 1)

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
        print(f"[DEBUG]: Task 8 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_both_odd(self):
    assert self.fun(3, 1) == "Yes"
    assert self.fun(1, 3) == "Yes"
    assert self.fun(3, 3) == "Yes"
    assert self.fun(1, 1) == "Yes"

  def test_02_one_even(self):
    assert self.fun(2, 1) == "No"
    assert self.fun(1, 2) == "No"
    assert self.fun(2, 3) == "No"
    assert self.fun(3, 2) == "No"

  def test_03_both_even(self):
    assert self.fun(2, 2) == "No"

  def test_04_boundary_values(self):
    assert self.fun(1, 1) == "Yes"
    assert self.fun(3, 3) == "Yes"

  def test_05_mixed_cases(self):
    assert self.fun(1, 3) == "Yes"
    assert self.fun(2, 2) == "No"