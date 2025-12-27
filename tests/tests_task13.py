class TestTask13:
  """Test Suite for HumanEval/10 - make_palindrome"""

  def __init__(self, make_palindrome):
    self.fun = make_palindrome

  def get_benchmark_input(self):
    return ('cat',)

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
        print(f"[DEBUG]: Task 13 - {method_name} failed.")
    
    return tests_passed, total_tests

  def test_01_empty_string(self):
    assert self.fun('') == ''

  def test_02_single_character(self):
    assert self.fun('x') == 'x'

  def test_03_no_palindrome_suffix(self):
    assert self.fun('xyz') == 'xyzyx'

  def test_04_already_palindrome(self):
    assert self.fun('xyx') == 'xyx'

  def test_05_longer_word(self):
    assert self.fun('jerry') == 'jerryrrej'

  def test_06_partial_palindrome_suffix(self):
    assert self.fun('cat') == 'catac'
    assert self.fun('cata') == 'catac'

  def test_07_all_same_chars(self):
    assert self.fun('aaa') == 'aaa'

  def test_08_two_chars_palindrome(self):
    assert self.fun('aa') == 'aa'
    
  def test_09_two_chars_different(self):
    assert self.fun('ab') == 'aba'
