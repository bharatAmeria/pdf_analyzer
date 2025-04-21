import os
from pathlib import Path

project_name = "src"

list_of_files = [
    f"{project_name}/constants/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/groq_handler.py",
    f"{project_name}/components/resume_analyzer.py",
    f"{project_name}/components/text_processor.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    "runPipeline.py",
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