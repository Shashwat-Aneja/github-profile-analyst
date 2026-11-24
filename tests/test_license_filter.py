from types import SimpleNamespace
from analyze_github import fetch_github_data

def test_license_filter_scopes_all_metrics_and_ranking():
    class Session:
        def get(self,url,**kwargs):
            payload=[{'name':'mit-repo','stargazers_count':5,'license':{'spdx_id':'MIT'}},{'name':'apache','stargazers_count':9,'license':{'spdx_id':'Apache-2.0'}},{'name':'unknown','stargazers_count':100,'license':None}] if url.endswith('/repos') else {}
            return SimpleNamespace(raise_for_status=lambda:None,json=lambda:payload)
    data=fetch_github_data('demo',session=Session(),licenses=['mit'],top_repositories=5)
    assert data['Total Stars']==5 and data['Analyzed Repositories']==1
    assert data['Top Repositories'][0]['name']=='mit-repo'
