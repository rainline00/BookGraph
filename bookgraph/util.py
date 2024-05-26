import re
from pathlib import Path


def remove_moves_from_sfen(sfen: str) -> str:
    """hash keyとしてsfen文字列を使うために、手数を取り除くためのメソッド"""
    return re.sub(r"\s\d+$", "", sfen)


def get_project_root() -> Path:
    return Path(__file__).parent.parent
