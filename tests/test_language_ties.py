import pytest
from analyze_github import fetch_github_data
from test_analyze_github import FakeResponse


@pytest.mark.parametrize("languages", [["Rust", "Python"], ["Python", "Rust"]])
def test_language_ties_do_not_depend_on_api_order(languages):
    class Session:
        def get(self, url, params=None, timeout=None):
            if url.endswith("/repos"):
                return FakeResponse([{"language": value} for value in languages])
            return FakeResponse({})
    assert fetch_github_data("demo", Session())["Most Used Language"] == "Python"
