import pytest
from analyze_github import _validate_repository_page
@pytest.mark.parametrize('value',['false',0,None,[]])
def test_malformed_archived_flags_are_rejected(value):
    with pytest.raises(ValueError,match='archived'):_validate_repository_page([{'archived':value}],1)
def test_boolean_archived_flag_is_valid():
    assert _validate_repository_page([{'archived':False}],1)==[{'archived':False}]
