import pytest

def test_check_len_of_text():
    phrase = input('Set a phrase:')
    assert len(phrase) < 15, 'Text longer than 15 characters'