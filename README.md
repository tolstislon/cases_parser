# Cases Parser

Creating an excel file with a description of test cases

## Start
1. clone repository
2. create file `config.ini`
3. `pipenv install`
4. `pipenv shell`
5. `python app.py`


## config.ini
```ini
[jira]
# Url jira server (Required)
url = https://jira.server.com/

# Username for Jira (Required)
user = username

# Password for Jira (Required)
password = password


[project]
# The path to the project (Required)
path = path

# Case folder (Optional default: cases)
cases = cases
```