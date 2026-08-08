def build_bullet_optimize_prompt(raw_bullet: str, job_description: str | None = None) -> tuple[str, str]:
    system_prompt = (
        "You are a resume writing assistant. You rewrite resume bullets using the "
        "XYZ formula (Accomplished X, measured by Y, by doing Z). "
        "CRITICAL RULE: Never invent numbers, percentages, or metrics that are not "
        "explicitly present in the user's input. If no metric is given, use a "
        "placeholder like [X%] or [Y hours] instead of making one up. "
        "Always respond in valid JSON with a single key 'rewritten' containing the rewritten bullet."
    )

    user_prompt = f'Rewrite this resume bullet: "{raw_bullet}"'
    if job_description:
        user_prompt += f'\n\nTailor it toward this job description if relevant:\n{job_description}'

    return system_prompt, user_prompt


def build_project_from_github_prompt(repo_data: dict) -> tuple[str, str]:
    system_prompt = (
        "You are a resume writing assistant. Given a GitHub repository's metadata and README, "
        "generate a resume project entry AND a categorized skills breakdown. "
        "Write 2-4 achievement-focused bullets using the XYZ formula "
        "(Accomplished X, measured by Y, by doing Z). "
        "CRITICAL RULE: Never invent numbers, percentages, users, or metrics not clearly supported by "
        "the README content. If no real metric exists, describe the technical achievement without a "
        "fabricated number — write a clean qualitative bullet instead, do not use a placeholder like [X%]. "
        "Never claim the project is 'production', 'live', or has real users unless the README says so. "
        "For skills, only include languages/frameworks/tools that are clearly used in this repo "
        "(from the detected languages and README) — do not invent technologies not evidenced by the data. "
        "Group skills into standard resume categories such as 'Languages', 'Frameworks/Libraries', "
        "'Databases', 'Tools/Platforms' — only include categories that actually apply to this repo. "
        "Respond in valid JSON with exactly these keys: "
        '"name" (string), "tags" (comma-separated string of the main technologies), '
        '"bullets" (array of 2-4 strings), '
        '"skills" (array of objects, each with "category" (string) and "items" (array of strings)).'
    )

    user_prompt = (
        f"Repository name: {repo_data['name']}\n"
        f"Description: {repo_data['description']}\n"
        f"Languages/tech detected: {', '.join(repo_data['languages'])}\n"
        f"README:\n{repo_data['readme']}"
    )

    return system_prompt, user_prompt


def build_skills_from_languages_prompt(languages: list[str]) -> tuple[str, str]:
    system_prompt = (
        "You are a resume writing assistant. Given a list of programming languages and "
        "technologies detected across a developer's GitHub repositories, organize them into "
        "standard resume skill categories such as 'Languages', 'Frameworks/Libraries', "
        "'Databases', 'Tools/Platforms'. "
        "CRITICAL RULE: Only include items from the provided list — do not add, infer, or "
        "invent any technology not explicitly given. "
        "Respond in valid JSON with exactly this shape: "
        '{"skills": [{"category": "string", "items": ["string", ...]}, ...]}.'
    )
    user_prompt = f"Technologies detected: {', '.join(languages)}"
    return system_prompt, user_prompt