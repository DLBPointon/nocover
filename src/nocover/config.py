import json
from pathlib import Path

class Config:
    def __init__(self, config_path: str):
        self.path: str              = str(Path(config_path).resolve())
        config_data: dict[str, str] = self.config_check() #self.read_config()
        self.email: str             = self.get_item(config_data, 'EMAIL')
        self.token: str             = self.get_item(config_data, 'HARDCOVER_API_TOKEN')
        self.db_url: str            = "https://api.hardcover.app/v1/graphql"


    def get_item(self, config_dict, config_key):
        return (
            config_dict[config_key]
            if isinstance(config_dict, dict) and len(config_dict.values()) > 0
            else False
        )


    def check_files(self):
        list_files = [
            "/series_list.csv", "/list_list.csv", "/prompt_list.csv"
        ]
        for i in list_files:
            full_path = self.path + i
            if not Path(self.path + i).exists():
                Path(full_path).write_text("")


    def config_check(self):
        full_path=f"{self.path}/.config"
        if Path(full_path).is_file():
            self.check_files()
            return self.read_config(full_path)
        else:
            self.check_files()
            Path(full_path).write_text("")
            return False


    def read_config(self, full_path):
        try:
            with open(full_path) as config_json:
                return json.load(fp=config_json)
        except:
            return False
