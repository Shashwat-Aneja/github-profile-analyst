import requests
import pytest

from analyze_github import fetch_github_data


class FakeResponse:
    def __init__(self, payload, error=None):
        self.payload = payload
        self.error = error

    def raise_for_status(self):
        if self.error:
            raise self.error

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self):
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params, timeout))
        if url.endswith("/repos"):
            page = params["page"]
            if page == 1:
                return FakeResponse([
                    {"stargazers_count": index, "language": "Python" if index <= 60 else "JavaScript"}
                    for index in range(1, 101)
                ])
            return FakeResponse([
                {"stargazers_count": 2, "language": "Python"},
                {"stargazers_count": 3, "language": None},
            ])
        return FakeResponse({
            "name": "Demo User",
            "public_repos": 102,
            "followers": 12,
            "following": 8,
        })


def test_fetch_github_data_aggregates_all_repository_pages():
    session = FakeSession()

    stats = fetch_github_data("demo-user", session=session)

    assert stats["Total Stars"] == 5055
    assert stats["Most Used Language"] == "Python"
    assert stats["Public Repositories"] == 102
    assert stats["Original Repositories"] == 102
    assert stats["Forked Repositories"] == 0
    assert len(session.calls) == 3
    assert all(call[2] == 10 for call in session.calls)


def test_fetch_github_data_propagates_http_errors():
    class FailingSession:
        def get(self, url, params=None, timeout=None):
            return FakeResponse({}, error=requests.HTTPError("rate limited"))

    with pytest.raises(requests.HTTPError, match="rate limited"):
        fetch_github_data("demo-user", session=FailingSession())


def test_empty_language_metadata_has_safe_fallback():
    class EmptyLanguageSession:
        def get(self, url, params=None, timeout=None):
            if url.endswith("/repos"):
                return FakeResponse([{"stargazers_count": 0, "language": None}])
            return FakeResponse({"public_repos": 1, "followers": 0, "following": 0})

    stats = fetch_github_data("demo-user", session=EmptyLanguageSession())

    assert stats["Most Used Language"] == "Not available"


def test_repository_summary_distinguishes_forks_from_originals():
    class ForkAwareSession:
        def get(self, url, params=None, timeout=None):
            if url.endswith("/repos"):
                return FakeResponse([
                    {"fork": False, "stargazers_count": 4, "language": "Python"},
                    {"fork": True, "stargazers_count": 2, "language": "Python"},
                    {"fork": False, "stargazers_count": 1, "language": "Rust"},
                ])
            return FakeResponse({"public_repos": 3, "followers": 0, "following": 0})

    stats = fetch_github_data("demo-user", session=ForkAwareSession())

    assert stats["Original Repositories"] == 2
    assert stats["Forked Repositories"] == 1
