class TestTask20:
  """Test Suite for longest_common_subsequence"""

  def __init__(self, longest_common_subsequence):
    self.fun = longest_common_subsequence

  def get_benchmark_input(self):
    return ("ABCDGH", "AEDFHR")

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
        print(f"[DEBUG]: Task 20 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_cases(self):
    assert self.fun("ABCDGH", "AEDFHR") == 3  # ADH
    assert self.fun("AGGTAB", "GXTXAYB") == 4  # GTAB

  def test_02_identical_strings(self):
    assert self.fun("ABC", "ABC") == 3

  def test_03_no_common_subsequence(self):
    assert self.fun("ABC", "XYZ") == 0

  def test_04_empty_strings(self):
    assert self.fun("", "") == 0
    assert self.fun("ABC", "") == 0
    assert self.fun("", "ABC") == 0

  def test_05_single_character(self):
    assert self.fun("A", "A") == 1
    assert self.fun("A", "B") == 0

  def test_06_one_is_subsequence(self):
    assert self.fun("AC", "ABC") == 2
    assert self.fun("ABC", "AXXBXXC") == 3

  def test_07_repeated_characters(self):
    assert self.fun("AAAA", "AA") == 2
    assert self.fun("ABAB", "BABA") == 3

  def test_08_longer_strings(self):
    assert self.fun("ABCDEFGHIJ", "ACEGIK") == 5  # ACEGI

  def test_09_case_sensitive(self):
    assert self.fun("abc", "ABC") == 0
