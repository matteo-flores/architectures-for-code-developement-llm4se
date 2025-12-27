class TestTask12:
  """Test Suite for HumanEval/7 - filter_by_substring"""

  def __init__(self, filter_by_substring):
    self.fun = filter_by_substring

  def get_benchmark_input(self):
    return (['abc', 'bacd', 'cde', 'array'], 'a')

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
        print(f"[DEBUG]: Task 12 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_cases(self):
    assert self.fun([], 'john') == []
    assert self.fun(['xxx', 'asd', 'xxy', 'john doe', 'xxxAAA', 'xxx'], 'xxx') == ['xxx', 'xxxAAA', 'xxx']

  def test_02_partial_match(self):
    assert self.fun(['xxx', 'asd', 'aaaxxy', 'john doe', 'xxxAAA', 'xxx'], 'xx') == ['xxx', 'aaaxxy', 'xxxAAA', 'xxx']

  def test_03_substring_in_middle(self):
    assert self.fun(['grunt', 'trumpet', 'prune', 'gruesome'], 'run') == ['grunt', 'prune']

  def test_04_empty_list(self):
    assert self.fun([], 'a') == []

  def test_05_no_matches(self):
    assert self.fun(['apple', 'banana', 'cherry'], 'xyz') == []

  def test_06_all_matches(self):
    assert self.fun(['test', 'testing', 'contest'], 'test') == ['test', 'testing', 'contest']

  def test_07_empty_substring(self):
    result = self.fun(['a', 'b', 'c'], '')
    assert result == ['a', 'b', 'c']

  def test_08_case_sensitive(self):
    assert self.fun(['Apple', 'apple', 'APPLE'], 'apple') == ['apple']
