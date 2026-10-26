import argparse

import requests

USERNAME = "Shashwat-Aneja"
API_TIMEOUT_SECONDS = 10
REPOSITORIES_PER_PAGE = 100


def fetch_github_data(username, session=None):
    """Fetch profile statistics and all public repositories with bounded requests."""
    client = session or requests
    api_url = f"https://api.github.com/users/{username}"
    repos_url = f"{api_url}/repos"

    profile_response = client.get(api_url, timeout=API_TIMEOUT_SECONDS)
    profile_response.raise_for_status()
    user_data = profile_response.json()
    if not isinstance(user_data, dict):
        raise ValueError("GitHub profile response was not a JSON object.")

    repos_data = []
    page = 1
    while True:
        response = client.get(
            repos_url,
            params={"per_page": REPOSITORIES_PER_PAGE, "page": page, "type": "owner"},
            timeout=API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        page_repositories = response.json()
        if not isinstance(page_repositories, list):
            raise ValueError("GitHub repositories response was not a JSON array.")
        repos_data.extend(page_repositories)
        if len(page_repositories) < REPOSITORIES_PER_PAGE:
            break
        page += 1

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    forked_repositories = sum(1 for repo in repos_data if repo.get("fork") is True)
    original_repositories = len(repos_data) - forked_repositories
    languages = {}
    for repo in repos_data:
        language = repo.get("language")
        if language:
            languages[language] = languages.get(language, 0) + 1

    most_used_language = max(languages, key=languages.get) if languages else "Not available"
    return {
        "Username": username,
        "Name": user_data.get("name") or "Not available",
        "Public Repositories": user_data.get("public_repos", "Not available"),
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
    args = parser.parse_args(argv)
    print("Fetching GitHub data...")
    try:
        stats = fetch_github_data(args.username)
    except (requests.RequestException, ValueError) as exc:
        parser.exit(1, f"Error fetching GitHub profile: {exc}\n")
    display_data(stats)


if __name__ == "__main__":
    main()
