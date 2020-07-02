from typing import List, Dict
from pathlib import Path
import sqlite3
from .config import Config
import requests
import logging

logger = logging.getLogger(__package__)


def sort_codes(value: Dict[str, str]) -> int:
    prefix, num = value['id'].split('-')
    return int(num)


def load_data(issues: List[str], config: Config):
    logger.info('Load issues data')
    database_path = Path('database.sqlite').absolute()
    exists = database_path.exists()
    data = []
    with sqlite3.connect(str(database_path), detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        logger.debug(f'Create connect: {database_path}')
        conn.row_factory = sqlite3.Row
        cr = conn.cursor()
        logger.debug('Create cursor')
        try:
            if not exists:
                logger.debug('Create table')
                cr.execute(
                    """CREATE TABLE issues (
                       id   STRING PRIMARY KEY ON CONFLICT ROLLBACK,
                       name TEXT,
                       url  STRING)
                    """
                )
                conn.commit()

            logger.debug('Check issues')
            for issue in issues:
                cr.execute('SELECT * FROM issues WHERE id=?', (issue,))
                if result := cr.fetchone():
                    logger.debug(f'{issue} get database')
                    data.append(dict(result))
                else:
                    logger.debug(f'{issue} get jira')
                    response = requests.get(
                        url=config.get_endpoint(issue),
                        auth=config.get_auth(),
                        params={'fields': 'summary'}
                    )
                    issue_data = {
                        'id': issue,
                        'name': response.json()['fields']['summary'],
                        'url': config.get_issue_url(issue)
                    }

                    cr.execute('INSERT INTO issues (id, name, url) VALUES (:id, :name, :url)', issue_data)
                    data.append(issue_data)
        finally:
            conn.commit()
            cr.close()
    data.sort(key=sort_codes)
    return data
