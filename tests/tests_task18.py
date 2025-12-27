class TestTask18:
  """Test Suite for CodeNet/p03759 - is_beautiful_arrangement"""

  def __init__(self, is_beautiful):
    self.fun = is_beautiful

  def get_benchmark_input(self):
    return (2, 4, 6)

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
        print(f"[DEBUG]: Task 18 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_beautiful(self):
    result = self.fun(2, 4, 6)
    assert result == "YES" or result == True

  def test_02_not_beautiful(self):
    result = self.fun(2, 5, 6)
    assert result == "NO" or result == False

  def test_03_all_same_height(self):
    result = self.fun(5, 5, 5)
    assert result == "YES" or result == True

  def test_04_descending_arithmetic(self):
    result = self.fun(9, 6, 3)
    assert result == "YES" or result == True

  def test_05_zero_middle(self):
    result = self.fun(1, 0, -1)
    assert result == "YES" or result == True

  def test_06_large_numbers(self):
    result = self.fun(100, 200, 300)
    assert result == "YES" or result == True

  def test_07_not_arithmetic(self):
    result = self.fun(1, 2, 4)
    assert result == "NO" or result == False

  def test_08_negative_numbers(self):
    result = self.fun(-6, -4, -2)
    assert result == "YES" or result == True
