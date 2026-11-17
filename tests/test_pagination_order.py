from analyze_github import fetch_github_data
from test_analyze_github import FakeResponse


def test_repository_pages_use_stable_name_order():
    class Session:
        def get(self, url, params=None, timeout=None):
            if url.endswith("/repos"):
                assert params["sort"] == "full_name"
                assert params["direction"] == "asc"
                return FakeResponse([])
            return FakeResponse({})
    assert fetch_github_data("demo", Session())["Original Repositories"] == 0
