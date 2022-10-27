from src.user_interface.home_page import HomePage

class TestIsEven:
    def test_even(self):
        component = HomePage()
        evenVal = 2

        actual = component.is_even(evenVal)
        expected = True
        
        assert actual is expected

    def test_odd(self):
        component = HomePage()
        evenVal = 1
        
        actual = component.is_even(evenVal)
        expected = False
        
        assert actual is expected

class TestInRange:
    def test_lower_bound(self):
        component = HomePage()
        lower_val = 3

        actual = component.in_range(lower_val)
        expected = False
        
        assert actual is expected
    
    def test_upper_bound(self):
        component = HomePage()
        upper_val = 8

        actual = component.in_range(upper_val)
        expected = False
        
        assert actual is expected
    
    def test_within_bounds(self):
        component = HomePage()
        within_range_val = 5

        actual = component.in_range(within_range_val)
        expected = True
        
        assert actual is expected

