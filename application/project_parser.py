import logging
import re
from pathlib import Path
from typing import List

from .user_types import Config

logger = logging.getLogger(__package__)


def parse_file(path: Path) -> List[str]:
    codes = []
    with path.open('r', encoding='utf-8') as file:
        for line in file:
            if math := re.match(r"@zephyr\((:?\'|\")(?P<code>\w+-\d+)(:?\'|\"\))", line):
                if code := math.group('code'):
                    codes.append(code)
    return codes


def parser(config: Config) -> List[str]:
    root = Path(config.project_path).absolute()
    logger.info(f'Parsing project: {root}')
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f'Invalid project path: "{root}"')
    cases = root.joinpath(config.project_cases)
    if not cases.exists() or not cases.is_dir():
        raise FileNotFoundError(f'Invalid cases path: "{cases}"')
    all_codes = []
    for file in cases.rglob('*.py'):
        all_codes.extend(parse_file(file))
    return all_codes
