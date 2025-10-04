import sys
import requests


def get_remote_data(query: str, token: str, url: str):
    """
    Get data from Hardcover API
    """
    reqHeaders = {'Authorization': token}

    response = requests.post(url=url, headers=reqHeaders, json={"query": query})

    if response.status_code == 200:
        return response.json()["data"]
    else:
        issue = "HARDCOVER API ACESS : Check your Token and Slug!"
        sys.exit(issue)
