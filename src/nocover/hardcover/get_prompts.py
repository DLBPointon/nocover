from nocover.config import Config

from nocover.hardcover.get_data import GetData


class PromptData(GetData):
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        super().__init__(query, api_path, config_path, offline)

        self.slugs: list[str] = self.get_list_slugs()
        self.lists = self.reformat_data_by_dict()
