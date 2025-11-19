import requests

# Change this to your GitHub username
USERNAME = "Shashwat-Aneja"

def fetch_github_data(username):
    api_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"

    user_data = requests.get(api_url).json()
    repos_data = requests.get(repos_url).json()

    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
    languages = {}

    for repo in repos_data:
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    most_used_language = max(languages, key=languages.get) if languages else "Not available"

    return {
        "Username": username,
        "Name": user_data.get("name", "Not available"),
        "Public Repositories": user_data.get("public_repos", "Not available"),
        "Followers": user_data.get("followers", "Not available"),
        "Following": user_data.get("following", "Not available"),
        "Total Stars": total_stars,
        "Most Used Language": most_used_language
    }

def display_data(data):
    print("\n=== GitHub Profile Analysis ===")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("================================\n")

if __name__ == "__main__":
    print("Fetching GitHub data...")
    stats = fetch_github_data(USERNAME)
    display_data(stats)
