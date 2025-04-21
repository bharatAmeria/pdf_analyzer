import os
from pathlib import Path

project_name = "src"

list_of_files = [
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/groq_handler.py",
    f"{project_name}/components/resume_analyzer.py",
    f"{project_name}/components/text_processor.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/config.py",
    f"{project_name}/utils/file_utils.py",
    f"{project_name}/utils/logger.py",
    f"{project_name}/utils/prompt_loader.py",
    ".github/workflows/ci-cd.yml",
    ".env",
    ".dockerignore",
    ".project-root",
    "lambda_handler.py",
    "prompts/prompts.json",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    "setup.py",
    "pyproject.toml",
    "testEnvironment.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")