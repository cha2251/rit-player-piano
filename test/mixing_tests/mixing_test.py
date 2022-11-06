from src.mixing.mixing import Mixing

class TestIsEven:
    def test_even(self):
        component = Mixing()
        evenVal = 2

        actual = True
        expected = True
        
        assert actual is expected

