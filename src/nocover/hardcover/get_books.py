from nocover.config import Config

from nocover.hardcover.get_data import GetData


class BookData(GetData):
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        super().__init__(query, api_path, config_path, offline)

        self.statuses: list[str] = self.get_statuses()
        self.dict_by_status = self.dict_by_status()
        self.structured_data = [self.restructured_data(data = i) for i in self.data]


    def restructured_data(self, data):
        cleaned = dict()
        key: str = data["book"]["title"]

        cleaned[key] = data["book"]
        cleaned[key]["user_status"] = data["user_book_status"]["slug"]
        return cleaned


    def get_statuses(self) -> list[str]:
        statuses = []
        for i in self.data:
            if i["user_book_status"]["slug"] not in statuses:
                statuses.append(i["user_book_status"]["slug"])

        return statuses


    def dict_by_status(self):
        sorted_dict = {}
        for status in self.statuses:
            for i in self.data:
                if status == i["user_book_status"]["slug"]:
                    if not sorted_dict.get(status):
                        sorted_dict[status] = dict()
                    key: str = i["book"]["title"]
                    sorted_dict[status][key] = i["book"]

        return sorted_dict
