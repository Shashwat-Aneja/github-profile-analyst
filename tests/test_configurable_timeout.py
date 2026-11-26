from types import SimpleNamespace
import pytest
from analyze_github import fetch_github_data

def test_timeout_applies_to_profile_and_repository_requests():
    class Session:
        calls=[]
        def get(self,url,**kwargs):
            self.calls.append(kwargs['timeout'])
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:[] if url.endswith('/repos') else {})
    session=Session();fetch_github_data('demo',session=session,timeout_seconds=2.5)
    assert session.calls==[2.5,2.5]

@pytest.mark.parametrize('value',[0,-1,121,float('nan'),True])
def test_invalid_timeout_fails_before_requests(value):
    with pytest.raises(ValueError,match='timeout_seconds'):fetch_github_data('demo',session=object(),timeout_seconds=value)
