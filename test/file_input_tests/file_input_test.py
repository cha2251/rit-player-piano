from src.file_input.file_input import FileInput

class TestIsEven:
    def test_even(self):
        component = FileInput()
        evenVal = 2

        actual = component.is_even(evenVal)
        expected = True
        
        assert actual is expected

    def test_odd(self):
        component = FileInput()
        evenVal = 1
        
        actual = component.is_even(evenVal)
        expected = False
        
        assert actual is expected

class TestInRange:
    def test_lower_bound(self):
        component = FileInput()
        lower_val = 3

        actual = component.in_range(lower_val)
        expected = False
        
        assert actual is expected
    
    def test_upper_bound(self):
        component = FileInput()
        upper_val = 8

        actual = component.in_range(upper_val)
        expected = False
        
        assert actual is expected
    
    def test_within_bounds(self):
        component = FileInput()
        within_range_val = 5

        actual = component.in_range(within_range_val)
        expected = True
        
        assert actual is expected

