class TestTask15:
  """Test Suite for MBPP/32 - max_Prime_Factors"""

  def __init__(self, max_Prime_Factors):
    self.fun = max_Prime_Factors

  def get_benchmark_input(self):
    return (15,)

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
        print(f"[DEBUG]: Task 15 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_basic_cases(self):
    assert self.fun(15) == 5
    assert self.fun(6) == 3
    assert self.fun(2) == 2

  def test_02_prime_number(self):
    assert self.fun(13) == 13
    assert self.fun(17) == 17

  def test_03_power_of_two(self):
    assert self.fun(8) == 2
    assert self.fun(16) == 2
    assert self.fun(32) == 2

  def test_04_large_prime_factor(self):
    assert self.fun(77) == 11  # 77 = 7 * 11
    assert self.fun(91) == 13  # 91 = 7 * 13

  def test_05_composite_with_repeated_factors(self):
    assert self.fun(12) == 3   # 12 = 2^2 * 3
    assert self.fun(18) == 3   # 18 = 2 * 3^2
    assert self.fun(50) == 5   # 50 = 2 * 5^2

  def test_06_larger_numbers(self):
    assert self.fun(100) == 5  # 100 = 2^2 * 5^2
    assert self.fun(1000) == 5 # 1000 = 2^3 * 5^3

  def test_07_product_of_two_primes(self):
    assert self.fun(35) == 7   # 35 = 5 * 7
    assert self.fun(143) == 13 # 143 = 11 * 13
