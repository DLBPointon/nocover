import os
import json

class Config:
    def __init__(self, config_path: str):
        self.path: str              = os.path.abspath(config_path)
        config_data: dict[str, str] = self.read_config()
        self.email: str             = config_data['EMAIL']
        self.token: str             = config_data['HARDCOVER_API_TOKEN']
        self.db_url: str            = "https://api.hardcover.app/v1/graphql"

    def read_config(self) -> dict[str, str]:
        with open(self.path + "/configs.json") as config_json:
            return json.load(fp=config_json)
