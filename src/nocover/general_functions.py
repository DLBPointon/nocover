import sys
from typing import Any
import requests
import json


def max_key_len(data_keys: list[str]) -> int:
    return max(len(k) for k in data_keys)


def json_dump(data, file) -> None:
    """
    To make sure all json.dumps are the same
    """
    json.dump(
        obj=data,
        fp=file,
        sort_keys=True,
        indent=4,  # HARD MUST, NO 2 SPACE INDENTS
    )


def get_remote_data(query: str, token: str, url: str) -> Any:
    """
    Get data from Hardcover API
    """
    reqHeaders = {"Authorization": token}

    response = requests.post(url=url, headers=reqHeaders, json={"query": query})

    if response.status_code == 200:
        return response.json()["data"]
    else:
        issue = "HARDCOVER API ACESS : Check your Token and Slug!"
        sys.exit(issue)
