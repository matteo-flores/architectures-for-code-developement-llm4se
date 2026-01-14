class TestTask19:
    """Test Suite for CodeNet/p03962 - count_different_colors"""

    def __init__(self, count_colors):
        self.fun = count_colors

    def get_benchmark_input(self):
        # CORRETTO: Restituisce una lista come unico argomento
        return ([3, 1, 4],)

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
                print(f"[DEBUG]: Task 19 - {method_name} failed: {e}")
        
        return tests_passed, total_tests

    def test_01_all_different(self):
        # 3 colori diversi -> 3
        assert self.fun([3, 1, 4]) == 3

    def test_02_all_same(self):
        # 3 colori uguali -> 1
        assert self.fun([5, 5, 5]) == 1

    def test_03_two_same(self):
        # 2 colori uguali, 1 diverso -> 2
        assert self.fun([1, 2, 1]) == 2
        assert self.fun([3, 3, 5]) == 2
        assert self.fun([7, 2, 2]) == 2

    def test_04_boundary_values(self):
        assert self.fun([1, 1, 1]) == 1
        assert self.fun([100, 100, 100]) == 1

    def test_05_min_max_values(self):
        assert self.fun([1, 50, 100]) == 3

    def test_06_consecutive_numbers(self):
        assert self.fun([1, 2, 3]) == 3

    def test_07_first_two_same(self):
        assert self.fun([10, 10, 20]) == 2

    def test_08_last_two_same(self):
        assert self.fun([10, 20, 20]) == 2