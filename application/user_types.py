from dataclasses import dataclass
from typing import Tuple


@dataclass
class Config:
    jira_url: str
    jira_user: str
    jira_password: str
    jira_issue_path: str
    jira_endpoint: str
    project_path: str
    project_cases: str

    def __post_init__(self):
        if self.jira_url.endswith('/'):
            self.jira_url = self.jira_url[:-1]
        if not self.jira_issue_path.startswith('/'):
            self.jira_issue_path = f'/{self.jira_issue_path}'
        if not self.jira_issue_path.endswith('/'):
            self.jira_issue_path = f'{self.jira_issue_path}/'
        if not self.jira_endpoint.startswith('/'):
            self.jira_endpoint = f'/{self.jira_endpoint}'
        if '@' in self.jira_user:
            raise ValueError('You must specify a username and not an email')

    def get_issue_url(self, issue: str) -> str:
        return f'{self.jira_url}{self.jira_issue_path}{issue}'

    def get_endpoint(self, issue: str) -> str:
        endpoint = self.jira_endpoint.format(issue_key=issue)
        return f'{self.jira_url}{endpoint}'

    def get_auth(self) -> Tuple[str, str]:
        return self.jira_user, self.jira_password
