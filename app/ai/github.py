import requests
import base64
from app.core.config import settings

def _github_headers():
    headers = {}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    return headers


def fetch_github_repo_data(repo_url: str) -> dict:
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = parts[-2], parts[-1]
    repo = repo.removesuffix(".git")

    headers = _github_headers()

    repo_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
    if repo_resp.status_code != 200:
        raise ValueError(f"Could not fetch repo (status {repo_resp.status_code}) — check the URL is a public GitHub repo")
    repo_data = repo_resp.json()

    languages_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}/languages", headers=headers)
    languages = list(languages_resp.json().keys()) if languages_resp.status_code == 200 else []

    readme_content = ""
    readme_resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}/readme", headers=headers)
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
    username = profile_url.rstrip("/").split("/")[-1]
    if not username:
        raise ValueError("Invalid GitHub profile URL")

    headers = _github_headers()

    repos_resp = requests.get(
        f"https://api.github.com/users/{username}/repos",
        params={"per_page": 30, "sort": "updated", "type": "owner"},
        headers=headers,
    )
    if repos_resp.status_code != 200:
        raise ValueError(f"Could not fetch GitHub profile (status {repos_resp.status_code})")

    repos = [r for r in repos_resp.json() if not r.get("fork")]

    languages = set()
    for repo in repos:
        lang_resp = requests.get(
            f"https://api.github.com/repos/{username}/{repo['name']}/languages",
            headers=headers,
        )
        if lang_resp.status_code == 200:
            languages.update(lang_resp.json().keys())

    return sorted(languages)