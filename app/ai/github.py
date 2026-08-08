import requests
import base64


def fetch_github_repo_data(repo_url: str) -> dict:
    """
    Takes a GitHub repo URL like https://github.com/user/repo
    Returns repo metadata + README content (public repos, no auth needed,
    but GitHub's unauthenticated rate limit is 60 req/hour).
    """
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = parts[-2], parts[-1]

    repo_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}")
    if repo_resp.status_code != 200:
        raise ValueError(f"Could not fetch repo (status {repo_resp.status_code}) — check the URL is a public GitHub repo")
    repo_data = repo_resp.json()

    languages_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}/languages")
    languages = list(languages_resp.json().keys()) if languages_resp.status_code == 200 else []

    readme_content = ""
    readme_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}/readme")
    if readme_resp.status_code == 200:
        encoded = readme_resp.json().get("content", "")
        try:
            readme_content = base64.b64decode(encoded).decode("utf-8", errors="ignore")
        except Exception:
            readme_content = ""

    return {
        "name": repo_data.get("name", repo),
        "description": repo_data.get("description", "") or "",
        "languages": languages,
        "readme": readme_content[:4000],
        "url": repo_data.get("html_url", repo_url),
    }


def fetch_github_profile_languages(profile_url: str) -> list[str]:
    """
    Takes a GitHub profile URL like https://github.com/username
    Returns the union of languages used across the user's public,
    non-fork repos (capped at their most recently updated 30 repos
    to keep this fast and within rate limits).
    """
    username = profile_url.rstrip("/").split("/")[-1]
    if not username:
        raise ValueError("Invalid GitHub profile URL")

    repos_resp = requests.get(
        f"https://api.github.com/users/{username}/repos",
        params={"per_page": 30, "sort": "updated", "type": "owner"},
    )
    if repos_resp.status_code != 200:
        raise ValueError(f"Could not fetch GitHub profile (status {repos_resp.status_code})")

    repos = [r for r in repos_resp.json() if not r.get("fork")]

    languages = set()
    for repo in repos:
        lang_resp = requests.get(
            f"https://api.github.com/repos/{username}/{repo['name']}/languages"
        )
        if lang_resp.status_code == 200:
            languages.update(lang_resp.json().keys())

    return sorted(languages)