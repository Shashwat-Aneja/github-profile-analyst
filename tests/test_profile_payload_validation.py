import pytest

from analyze_github import fetch_github_data


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


class ProfileOnlySession:
    def __init__(self, profile):
        self.profile = profile
        self.repo_calls = 0

    def get(self, url, **_kwargs):
        if url.endswith("/repos"):
            self.repo_calls += 1
            return FakeResponse([])
        return FakeResponse(self.profile)


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("public_repos", -1),
        ("public_repos", True),
        ("followers", "42"),
        ("followers", 2.5),
        ("following", None),
    ],
)
def test_invalid_profile_counts_are_rejected_before_pagination(field, invalid):
    session = ProfileOnlySession(
        {"public_repos": 1, "followers": 2, "following": 3, field: invalid}
    )

    with pytest.raises(ValueError, match=field):
        fetch_github_data("demo-user", session=session)

    assert session.repo_calls == 0


def test_zero_profile_counts_are_accepted():
    session = ProfileOnlySession(
        {"public_repos": 0, "followers": 0, "following": 0}
    )

    summary = fetch_github_data("demo-user", session=session)

    assert summary["Public Repositories"] == 0
    assert summary["Followers"] == 0
    assert summary["Following"] == 0
    assert session.repo_calls == 1
