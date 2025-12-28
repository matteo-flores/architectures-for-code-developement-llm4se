class TestTask7:
  """Test Suite for CodeNet/p03149 - can_form_1974"""

  def __init__(self, can_form_1974):
    self.fun = can_form_1974

  def get_benchmark_input(self):
    return ([1, 7, 9, 4],)

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
        print(f"[DEBUG]: Task 7 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_cases(self):
    assert self.fun([1, 7, 9, 4]) == 'YES'
    assert self.fun([4, 9, 7, 1]) == 'YES'

  def test_02_invalid_cases(self):
    assert self.fun([1, 1, 9, 4]) == 'NO'
    assert self.fun([0, 1, 9, 4]) == 'NO'

  def test_03_all_permutations_valid(self):
    assert self.fun([9, 7, 4, 1]) == 'YES'
    assert self.fun([7, 1, 4, 9]) == 'YES'

  def test_04_missing_digit(self):
    assert self.fun([1, 9, 9, 4]) == 'NO'
    assert self.fun([7, 7, 9, 4]) == 'NO'

  def test_05_wrong_digits(self):
    assert self.fun([2, 3, 5, 6]) == 'NO'
    assert self.fun([1, 9, 7, 5]) == 'NO'

  def test_06_duplicate_digits(self):
    assert self.fun([1, 1, 1, 1]) == 'NO'
    assert self.fun([9, 9, 9, 9]) == 'NO'