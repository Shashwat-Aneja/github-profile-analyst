from test_push_date import session
from analyze_github import fetch_github_data

def test_star_distribution_reconciles_unknown_languages():
    data=fetch_github_data('demo',session=session([{'language':'Python','stargazers_count':6},{'language':None,'stargazers_count':4},{'language':'Rust','stargazers_count':0}]))
    assert data['Language Stars']=={'Python':6,'Rust':0}
    assert data['Unspecified Language Stars']==4 and data['Unspecified Language Repositories']==1
    assert sum(data['Language Stars'].values())+data['Unspecified Language Stars']==data['Total Stars']
