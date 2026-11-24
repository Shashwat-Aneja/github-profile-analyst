import pytest
from types import SimpleNamespace
from analyze_github import fetch_github_data

def test_page_budget_fails_without_requesting_or_reporting_a_partial_next_page():
    class Session:
        calls=0
        def get(self,url,**kwargs):
            self.calls+=1
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:[{'stargazers_count':0} for _ in range(100)] if url.endswith('/repos') else {})
    session=Session()
    with pytest.raises(ValueError,match='page limit'):fetch_github_data('demo',session=session,max_pages=1)
    assert session.calls==2

@pytest.mark.parametrize('limit',[0,1001,True])
def test_invalid_budget_precedes_network(limit):
    with pytest.raises(ValueError,match='max_pages'):fetch_github_data('demo',session=object(),max_pages=limit)
