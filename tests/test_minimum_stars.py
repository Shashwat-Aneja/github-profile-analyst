import pytest
from analyze_github import fetch_github_data
class Response:
    def __init__(self,data):self.data=data
    def raise_for_status(self):pass
    def json(self):return self.data
class Session:
    def get(self,url,**kwargs):return Response([{'stargazers_count':1,'language':'Rust'},{'stargazers_count':5,'language':'Python'}] if url.endswith('/repos') else {'public_repos':2})
def test_star_filter_changes_all_repository_metrics_consistently():
    data=fetch_github_data('demo',session=Session(),min_stars=5)
    assert data['Analyzed Repositories']==1 and data['Total Stars']==5
    assert data['Language Repositories']=={'Python':1} and data['Public Repositories']==2
def test_invalid_star_filter_fails_before_requests():
    with pytest.raises(ValueError):fetch_github_data('demo',session=object(),min_stars=-1)
