from src.button_input.button_input import ButtonInput

class TestIsEven:
    def test_even(self):
        component = ButtonInput()
        evenVal = 2

        actual = component.is_even(evenVal)
        expected = True
        
        assert actual is expected

    def test_odd(self):
        component = ButtonInput()
        evenVal = 1
        
        actual = component.is_even(evenVal)
        expected = False
        
        assert actual is expected

class TestInRange:
    def test_lower_bound(self):
        component = ButtonInput()
        lower_val = 3

        actual = component.in_range(lower_val)
        expected = False
        
        assert actual is expected
    
    def test_upper_bound(self):
        component = ButtonInput()
        upper_val = 8

        actual = component.in_range(upper_val)
        expected = False
        
        assert actual is expected
    
    def test_within_bounds(self):
        component = ButtonInput()
        within_range_val = 5

        actual = component.in_range(within_range_val)
        expected = True
        
        assert actual is expected

