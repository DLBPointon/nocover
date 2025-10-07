import json
from nocover.config import Config

from nocover.hardcover.get_data import GetData

from nocover.general_functions import get_remote_data

class ListData(GetData):
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        super().__init__(query, api_path, config_path, offline)

        slugs: list[str] = self.get_list_slugs()
