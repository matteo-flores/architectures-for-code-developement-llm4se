class TestTask14:
  """Test Suite for MBPP/12 - sort_matrix"""

  def __init__(self, sort_matrix):
    self.fun = sort_matrix

  def get_benchmark_input(self):
    return ([[1, 2, 3], [2, 4, 5], [1, 1, 1]],)

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
        print(f"[DEBUG]: Task 14 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_case(self):
    assert self.fun([[1, 2, 3], [2, 4, 5], [1, 1, 1]]) == [[1, 1, 1], [1, 2, 3], [2, 4, 5]]

  def test_02_negative_numbers(self):
    assert self.fun([[1, 2, 3], [-2, 4, -5], [1, -1, 1]]) == [[-2, 4, -5], [1, -1, 1], [1, 2, 3]]

  def test_03_different_order(self):
    assert self.fun([[5, 8, 9], [6, 4, 3], [2, 1, 4]]) == [[2, 1, 4], [6, 4, 3], [5, 8, 9]]

  def test_04_empty_matrix(self):
    assert self.fun([]) == []

  def test_05_single_row(self):
    assert self.fun([[5, 10, 15]]) == [[5, 10, 15]]

  def test_06_equal_sums(self):
    result = self.fun([[1, 2], [2, 1], [0, 3]])
    sums = [sum(row) for row in result]
    assert sums == sorted(sums)

  def test_07_all_zeros(self):
    assert self.fun([[0, 0], [0, 0], [0, 0]]) == [[0, 0], [0, 0], [0, 0]]

  def test_08_single_element_rows(self):
    assert self.fun([[5], [1], [3]]) == [[1], [3], [5]]
