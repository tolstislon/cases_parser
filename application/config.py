import configparser
from pathlib import Path

from .user_types import Config


def get_config():
    path = Path('.').absolute()
    for line in path.rglob('config.ini'):
        conf = configparser.ConfigParser()
        conf.read(str(line), encoding='utf-8')
        return Config(
            jira_url=conf.get('jira', 'url'),
            jira_user=conf.get('jira', 'user'),
            jira_password=conf.get('jira', 'password'),
            jira_issue_path=conf.get('jira', 'issue_path', fallback='/browse/'),
            jira_endpoint=conf.get('jira', 'endpoint', fallback='/rest/api/2/issue/{issue_key}'),
            project_cases=conf.get('project', 'cases', fallback='cases'),
            project_path=conf.get('project', 'path')
        )
    raise FileNotFoundError('Not found config.ini')
