from types import SimpleNamespace
import pytest
from analyze_github import fetch_github_data

class Session:
    def get(self, url, **kwargs):
        payload = [{"name": "zeta", "stargazers_count": 4}, {"name": "Alpha", "stargazers_count": 4}] if url.endswith('/repos') else {}
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: payload)

def test_ranking_is_deterministic_without_truncating_metrics():
    result = fetch_github_data('demo', session=Session(), top_repositories=1)
    assert result['Top Repositories'] == [{"name": "Alpha", "stars": 4, "language": None, "url": None}]
    assert result['Analyzed Repositories'] == 2
    assert result['Total Stars'] == 8

@pytest.mark.parametrize('limit', [-1, 101, True, 1.5])
def test_invalid_limit_precedes_network(limit):
    with pytest.raises(ValueError, match='top_repositories'):
        fetch_github_data('demo', session=object(), top_repositories=limit)
