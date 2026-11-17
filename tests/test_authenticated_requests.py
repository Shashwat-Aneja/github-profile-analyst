import pytest
from analyze_github import fetch_github_data
from test_analyze_github import FakeResponse


def test_token_is_only_sent_in_authorization_header():
    class Session:
        def get(self, url, **kwargs):
            assert "test-token" not in url
            assert kwargs["headers"] == {"Authorization": "Bearer test-token"}
            return FakeResponse([] if url.endswith("/repos") else {})
    assert fetch_github_data("demo", Session(), token="test-token")["Original Repositories"] == 0


@pytest.mark.parametrize("token", ["", "bad token", "bad\ntoken", True])
def test_invalid_token_rejected_before_request(token):
    class Session:
        def get(self, *args, **kwargs):
            raise AssertionError("must not make a request")
    with pytest.raises(ValueError, match="token"):
        fetch_github_data("demo", Session(), token=token)
