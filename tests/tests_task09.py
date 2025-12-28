class TestTask9:
  """Test Suite for CodeNet/p03466 - get_substring"""

  def __init__(self, get_substring):
    self.fun = get_substring

  def get_benchmark_input(self):
    return (2, 3, 1, 5)

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
        print(f"[DEBUG]: Task 9 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_cases(self):
    assert self.fun(2, 3, 1, 5) == "BABAB"
    assert self.fun(6, 4, 1, 10) == "AABAABAABB"

  def test_02_single_character(self):
    assert self.fun(2, 3, 4, 4) == "A"

  def test_03_substring_middle(self):
    assert self.fun(6, 4, 3, 7) == "BAABA"

  def test_04_another_case(self):
    assert self.fun(8, 10, 5, 8) == "ABAB"

  def test_05_full_string_small(self):
    result = self.fun(1, 1, 1, 2)
    assert len(result) == 2
    assert result.count('A') == 1
    assert result.count('B') == 1

  def test_06_more_as_than_bs(self):
    result = self.fun(3, 1, 1, 4)
    assert len(result) == 4
    assert result.count('A') == 3
    assert result.count('B') == 1