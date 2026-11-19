import argparse
import json
import os
import re

import requests

USERNAME = "Shashwat-Aneja"
USERNAME_PATTERN = re.compile(r"^(?!.*--)[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
API_TIMEOUT_SECONDS = 10
REPOSITORIES_PER_PAGE = 100
MAX_REPOSITORY_PAGES = 1000


def validate_username(username):
    """Reject values that cannot be GitHub account logins before making a request."""
    if not isinstance(username, str) or not USERNAME_PATTERN.fullmatch(username):
        raise ValueError(
            "GitHub username must be 1-39 characters, use letters, digits, or single hyphens, "
            "and cannot start or end with a hyphen."
        )
    return username


def _validate_repository_page(payload, page):
    """Validate GitHub repository records before aggregating profile statistics."""
    if not isinstance(payload, list):
        raise ValueError(f"GitHub repositories response on page {page} was not a JSON array.")

    if len(payload) > REPOSITORIES_PER_PAGE:
        raise ValueError(f"GitHub repositories response on page {page} exceeded the requested page size.")
    for index, repository in enumerate(payload, start=1):
        if not isinstance(repository, dict):
            raise ValueError(
                f"GitHub repository entry {index} on page {page} must be a JSON object."
            )
        repository_id = repository.get("id")
        if repository_id is not None and (isinstance(repository_id, bool) or not isinstance(repository_id, int) or repository_id < 1):
            raise ValueError(f"GitHub repository entry {index} on page {page} has an invalid id.")
        stars = repository.get("stargazers_count", 0)
        if isinstance(stars, bool) or not isinstance(stars, int) or stars < 0:
            raise ValueError(
                f"GitHub repository entry {index} on page {page} has an invalid stargazers_count."
            )
        fork = repository.get("fork", False)
        if not isinstance(fork, bool):
            raise ValueError(
                f"GitHub repository entry {index} on page {page} has an invalid fork flag."
            )
        if "archived" in repository and not isinstance(repository["archived"], bool):
            raise ValueError(f"GitHub repository entry {index} on page {page} has an invalid archived flag.")
        language = repository.get("language")
        if language is not None and not isinstance(language, str):
            raise ValueError(
                f"GitHub repository entry {index} on page {page} has an invalid language."
            )

    return payload


def request_with_retry(client, url, **options):
    """Retry transient, read-only API failures once; do not retry auth/rate limits."""
    for attempt in range(2):
        try:
            response = client.get(url, **options)
            response.raise_for_status()
            return response
        except (requests.Timeout, requests.ConnectionError):
            if attempt:
                raise
        except requests.HTTPError as exc:
            status = getattr(exc.response, "status_code", None)
            if attempt or status not in {500, 502, 503, 504}:
                raise


def fetch_github_data(username, session=None, exclude_forks=False, exclude_archived=False, token=None):
    """Fetch profile statistics and all public repositories with bounded requests."""
    validate_username(username)
    client = session or requests
    api_url = f"https://api.github.com/users/{username}"
    repos_url = f"{api_url}/repos"

    request_options = {"timeout": API_TIMEOUT_SECONDS}
    if token is not None:
        if not isinstance(token, str) or not token.strip() or any(char.isspace() for char in token):
            raise ValueError("GitHub token must be a non-empty token without whitespace.")
        request_options["headers"] = {"Authorization": f"Bearer {token}"}
    profile_response = request_with_retry(client, api_url, **request_options)
    user_data = profile_response.json()
    if not isinstance(user_data, dict):
        raise ValueError("GitHub profile response was not a JSON object.")
    for field in ("public_repos", "followers", "following"):
        if field in user_data:
            count = user_data[field]
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError(f"GitHub profile field {field} must be a non-negative integer.")

    repos_data = []
    seen_repository_ids = set()
    page = 1
    while True:
        if page > MAX_REPOSITORY_PAGES:
            raise ValueError("GitHub repository pagination exceeded the safety page limit.")
        response = request_with_retry(
            client, repos_url,
            params={"per_page": REPOSITORIES_PER_PAGE, "page": page, "type": "owner", "sort": "full_name", "direction": "asc"},
            **request_options,
        )
        page_repositories = _validate_repository_page(response.json(), page)
        for repository in page_repositories:
            repository_id = repository.get("id")
            if repository_id is not None:
                if repository_id in seen_repository_ids:
                    raise ValueError("GitHub repository pagination returned a duplicate repository id.")
                seen_repository_ids.add(repository_id)
        repos_data.extend(page_repositories)
        if len(page_repositories) < REPOSITORIES_PER_PAGE:
            break
        page += 1

    if exclude_forks:
        repos_data = [repository for repository in repos_data if not repository.get("fork", False)]
    if exclude_archived:
        repos_data = [repository for repository in repos_data if not repository.get("archived", False)]
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    forked_repositories = sum(1 for repo in repos_data if repo.get("fork") is True)
    original_repositories = len(repos_data) - forked_repositories
    languages = {}
    for repo in repos_data:
        language = repo.get("language")
        if language:
            languages[language] = languages.get(language, 0) + 1

    most_used_language = min(languages, key=lambda language: (-languages[language], language)) if languages else "Not available"
    return {
        "Username": username,
        "Name": user_data.get("name") or "Not available",
        "Public Repositories": user_data.get("public_repos", "Not available"),
        "Analyzed Repositories": len(repos_data),
        "Language Repositories": dict(sorted(languages.items())),
        "Original Repositories": original_repositories,
        "Forked Repositories": forked_repositories,
        "Followers": user_data.get("followers", "Not available"),
        "Following": user_data.get("following", "Not available"),
        "Total Stars": total_stars,
        "Most Used Language": most_used_language,
    }


def display_data(data):
    print("\n=== GitHub Profile Analysis ===")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("================================\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize a public GitHub profile.")
    parser.add_argument("username", nargs="?", default=USERNAME, help="GitHub username to analyze")
    parser.add_argument("--json", action="store_true", help="Print only a JSON profile summary")
    parser.add_argument("--exclude-forks", action="store_true", help="Exclude forks from repository metrics")
    parser.add_argument("--exclude-archived", action="store_true", help="Exclude archived repositories from metrics")
    args = parser.parse_args(argv)
    if not args.json:
        print("Fetching GitHub data...")
    try:
        options = {}
        if os.environ.get("GITHUB_TOKEN"):
            options["token"] = os.environ["GITHUB_TOKEN"]
        if args.exclude_forks:
            options["exclude_forks"] = True
        if args.exclude_archived:
            options["exclude_archived"] = True
        stats = fetch_github_data(args.username, **options)
    except (requests.RequestException, ValueError) as exc:
        parser.exit(1, f"Error fetching GitHub profile: {exc}\n")
    if args.json:
        print(json.dumps(stats, ensure_ascii=False))
    else:
        display_data(stats)


if __name__ == "__main__":
    main()
