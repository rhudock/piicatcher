import pytest

from .commonregex import CommonRegex


class TestRegex:
    def test_credit_card_regex(self):
        assert hasattr(CommonRegex('4012888888881881'), 'credit_cards') is True, print('CCN Test Failed')
