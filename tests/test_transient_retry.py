import requests
import pytest
from analyze_github import request_with_retry


def response(status):
    value = requests.Response()
    value.status_code = status
    value.url = "https://api.github.com/test"
    return value


@pytest.mark.parametrize("failure", [requests.Timeout(), requests.ConnectionError(), response(503)])
def test_transient_read_failure_is_retried_once(failure):
    class Session:
        calls = 0
        def get(self, url, **options):
            self.calls += 1
            if self.calls == 1:
                if isinstance(failure, Exception):
                    raise failure
                return failure
            return response(200)
    session = Session()
    assert request_with_retry(session, "https://api.github.com/test", timeout=10).status_code == 200
    assert session.calls == 2


@pytest.mark.parametrize("status, expected_calls", [(401, 1), (429, 1), (503, 2)])
def test_retry_budget_and_nonretryable_statuses(status, expected_calls):
    class Session:
        calls = 0
        def get(self, *args, **kwargs):
            self.calls += 1
            return response(status)
    session = Session()
    with pytest.raises(requests.HTTPError):
        request_with_retry(session, "https://api.github.com/test")
    assert session.calls == expected_calls
