from types import SimpleNamespace
import pytest
from analyze_github import fetch_github_data

def session(repos):
    class Session:
        def get(self,url,**kwargs):
            payload=repos if url.endswith('/repos') else {}
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:payload)
    return Session()

def test_push_date_is_inclusive_utc_and_applies_to_ranking():
    repos=[{"name":"old","stargazers_count":100,"pushed_at":"2026-11-27T00:30:00+05:30"},{"name":"new","stargazers_count":2,"pushed_at":"2026-11-26T23:00:00-02:00"},{"name":"empty","pushed_at":None}]
    data=fetch_github_data('demo',session=session(repos),pushed_since='2026-11-27',top_repositories=2)
    assert data['Total Stars']==2 and data['Top Repositories'][0]['name']=='new'

def test_bad_date_precedes_http():
    with pytest.raises(ValueError):fetch_github_data('demo',session=object(),pushed_since='2026-02-30')
