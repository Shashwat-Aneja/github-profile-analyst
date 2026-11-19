import pytest
from analyze_github import _validate_repository_page,REPOSITORIES_PER_PAGE
def test_oversized_page_fails_instead_of_overcounting():
    with pytest.raises(ValueError,match='page size'):_validate_repository_page([{}]*(REPOSITORIES_PER_PAGE+1),1)
