from analyze_github import fetch_github_data
class Response:
    def __init__(self,data):self.data=data
    def raise_for_status(self):pass
    def json(self):return self.data
class Session:
    def get(self,url,**kwargs):
        return Response([{'language':'Python'},{'language':'Rust','archived':True},{'language':None}]) if url.endswith('/repos') else Response({'public_repos':3})
def test_language_breakdown_and_analyzed_count_follow_filters():
    result=fetch_github_data('demo',session=Session(),exclude_archived=True)
    assert result['Public Repositories']==3
    assert result['Analyzed Repositories']==2
    assert result['Language Repositories']=={'Python':1}
