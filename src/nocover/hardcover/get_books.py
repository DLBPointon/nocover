import json
from nocover.config import Config
from nocover.general_functions import get_remote_data

class BookData:
    def __init__(self, query: str, config_path: Config, offline: bool):
        self.query: str          = query
        self.db_url: str         = config_path.db_url
        self.config: Config      = config_path
        self.offline: bool       = offline
        get_book_data       = (
            # self.get_local_data(config_path)
            # if offline else
            get_remote_data(query=query, token=self.config.token, url=self.db_url)
        )
        data = get_book_data["me"][0]["user_books"]

        self.statuses: list[str] = self.get_statuses(data)
        self.dict_by_status = self.dict_by_status(data=data, status_list=self.statuses)
        self.structured_data = [self.restructured_data(data = i) for i in data]

    def restructured_data(self, data):
        cleaned = dict()
        key: str = data["book"]["title"]

        cleaned[key] = data["book"]
        cleaned[key]["user_status"] = data["user_book_status"]["slug"]
        return cleaned


    def get_statuses(self, data) -> list[str]:
        statuses = []
        for i in data:
            if i["user_book_status"]["slug"] not in statuses:
                statuses.append(i["user_book_status"]["slug"])

        return statuses


    def dict_by_status(self, data, status_list: list[str]):
        sorted_dict = {}
        for status in status_list:
            for i in data:
                if status == i["user_book_status"]["slug"]:
                    if not sorted_dict.get(status):
                        sorted_dict[status] = dict()
                    key: str = i["book"]["title"]
                    sorted_dict[status][key] = i["book"]

        with open ("dict_test.json", "w") as f:
            json.dump(sorted_dict, f)

        return sorted_dict
