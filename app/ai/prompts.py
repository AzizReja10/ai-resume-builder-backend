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
        "generate a resume project entry, a categorized skills breakdown, and extract any personal "
        "profile links or education details the README author explicitly mentions about themselves. "
        "Write 2-4 achievement-focused bullets using the XYZ formula "
        "(Accomplished X, measured by Y, by doing Z). "
        "CRITICAL RULE: Never invent numbers, percentages, users, or metrics not clearly supported by "
        "the README content. If no real metric exists, describe the technical achievement without a "
        "fabricated number — write a clean qualitative bullet instead, do not use a placeholder like [X%]. "
        "Never claim the project is 'production', 'live', or has real users unless the README says so. "
        "For skills, only include languages/frameworks/tools clearly used in this repo. "
        "For profile_links: ONLY extract links the README explicitly contains (e.g. a 'Connect with me' "
        "or author bio section with LinkedIn, LeetCode, Codeforces, portfolio links). "
        "If the README contains no such links, return an empty list — do not guess or construct URLs. "
        "For education: ONLY extract it if the README explicitly states the author's university/degree/CGPA "
        "in an author bio or 'About me' section. Most READMEs will not have this — if absent, return an "
        "empty list. Never infer education from project subject matter. "
        "Respond in valid JSON with exactly these keys: "
        '"name" (string), "tags" (comma-separated string), "bullets" (array of strings), '
        '"skills" (array of {"category": string, "items": [string]}), '
        '"profile_links" (array of {"label": string, "url": string}), '
        '"education" (array of {"institution": string, "degree": string, "detail": string, "dates": string}).'
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
def build_resume_analysis_prompt(resume_text:str)->tuple[str,str]:
    system_prompt=("You are an experienced technical recruiter and resume reviewer. Analyze the resume text "
        "provided and give constructive, specific feedback. "
        "CRITICAL RULES: "
        "1. Base every observation strictly on what is actually written in the resume text. Never assume "
        "or invent details, achievements, or skills not present in the text. "
        "2. The score (0-100) should reflect clarity, use of quantified achievements, relevance of content, "
        "and overall structure — be honest and calibrated, not artificially generous. A generic or thin "
        "resume should score lower; a strong, specific, well-structured one should score higher. "
        "3. Improvements must be specific and actionable (e.g. 'Bullet 2 under Project X lacks a measurable "
        "outcome — consider adding a metric or scope' rather than vague advice like 'add more detail'). "
        "4. Do not fabricate what's missing — if the resume already has metrics, don't claim it lacks them. "
        "Respond in valid JSON with exactly these keys: "
        '"score" (integer 0-100), "summary" (string, 2-3 sentences), '
        '"strengths" (array of strings), "improvements" (array of strings), '
        '"section_feedback" (array of objects with "section" and "feedback" keys, '
        "one entry per resume section actually present, e.g. Education, Experience, Projects, Skills).")
    user_prompt=f"Resume text:\n\n{resume_text}"
    return system_prompt,user_prompt