from types import SimpleNamespace
from analyze_github import fetch_github_data

def test_repository_exclusions_scope_metrics_and_rankings():
    class Session:
        def get(self,url,**kwargs):
            payload=[{'name':'Web-Site','stargazers_count':100},{'name':'cli','stargazers_count':5}] if url.endswith('/repos') else {}
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:payload)
    result=fetch_github_data('demo',session=Session(),exclude_repositories=['web-*'],top_repositories=10)
    assert result['Analyzed Repositories']==1 and result['Total Stars']==5
    assert result['Top Repositories'][0]['name']=='cli'
