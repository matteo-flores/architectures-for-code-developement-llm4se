class TestTask16:
  """Test Suite for MBPP/316 - find_last_occurrence"""

  def __init__(self, find_last_occurrence):
    self.fun = find_last_occurrence

  def get_benchmark_input(self):
    return ([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5)

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
        print(f"[DEBUG]: Task 16 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_cases(self):
    assert self.fun([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 3
    assert self.fun([2, 3, 5, 8, 6, 6, 8, 9, 9, 9], 9) == 9
    assert self.fun([2, 2, 1, 5, 6, 6, 6, 9, 9, 9], 6) == 6

  def test_02_element_not_found(self):
    assert self.fun([1, 2, 3, 4, 5], 10) == -1
    assert self.fun([1, 2, 3, 4, 5], 0) == -1

  def test_03_single_element(self):
    assert self.fun([5], 5) == 0
    assert self.fun([5], 3) == -1

  def test_04_empty_array(self):
    assert self.fun([], 5) == -1

  def test_05_all_same_elements(self):
    assert self.fun([7, 7, 7, 7, 7], 7) == 4

  def test_06_first_element(self):
    assert self.fun([1, 2, 3, 4, 5], 1) == 0

  def test_07_last_element(self):
    assert self.fun([1, 2, 3, 4, 5], 5) == 4

  def test_08_multiple_occurrences_at_end(self):
    assert self.fun([1, 2, 3, 3, 3], 3) == 4
