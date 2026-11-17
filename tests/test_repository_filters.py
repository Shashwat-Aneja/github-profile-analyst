from analyze_github import fetch_github_data
from test_analyze_github import FakeResponse


def test_filters_apply_to_aggregates_without_changing_public_profile_count():
    class Session:
        def get(self, url, **kwargs):
            if url.endswith("/repos"):
                return FakeResponse([
                    {"fork": True, "stargazers_count": 100},
                    {"archived": True, "stargazers_count": 200},
                    {"language": "Python", "stargazers_count": 3},
                ])
            return FakeResponse({"public_repos": 3})
    result = fetch_github_data("demo", Session(), exclude_forks=True, exclude_archived=True)
    assert result["Total Stars"] == 3
    assert result["Original Repositories"] == 1
    assert result["Public Repositories"] == 3
