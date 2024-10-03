from atlassian import Jira
from requests import HTTPError

jira =Jira(
    url = "https://sptech-team-it55r942.atlassian.net",
    username = "felipe.patroni@sptech.school",
    password = "" #TOKEN
)

try:

    jira.issue_create(
        fields={
            'project': {
                'key': 'TRAC' #SIGLA
            },
            'summary': 'TESTE', #titulo do chamado
            'description': 'teste automação- descrição', #descrição
            'issuetype': {
                "name": "Task" #Tipo de chamado 
            },
        }
    )
except HTTPError as e :
    print(e.response.text)