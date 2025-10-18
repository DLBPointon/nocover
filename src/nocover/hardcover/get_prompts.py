import json
from nocover.config import Config

from nocover.hardcover.get_data import GetData

from nocover.general_functions import get_remote_data, json_dump

class PromptData(GetData):
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        super().__init__(query, api_path, config_path, offline)

        self.slugs: list[str] = self.get_list_slugs()
        self.lists = self.reformat_data_by_dict()
