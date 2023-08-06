from pathlib import Path


def get_project_root() -> Path:
    print(Path(__file__).parent.parent)
    return Path(__file__).parent.parent.parent


get_project_root()
