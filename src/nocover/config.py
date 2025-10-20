import json
from pathlib import Path

from nocover.modals.error_page import ErrorModal

class Config:
    def __init__(self, config_path: str):
        self.path: str                  = str(Path(config_path).resolve())
        config_data: dict[str, str]     = self.config_check() #self.read_config()
        self.default_folders: dict[str, str] = {
            "lists": self.path + "/list_data/",
            "series": self.path + "/series_data/",
            "prompts": self.path + "/prompt_data/",
            "logging": self.path + "/logs/"
        }

        self.index_file_dict: dict[str,str] = {
            "prompts": self.default_folders["prompts"] + "prompt_index.tsv",
            "lists": self.default_folders["lists"] + "list_index.tsv",
            "series": self.default_folders["series"] + "series_index.tsv"
        }
        self.email: str = self.get_item(config_data, 'EMAIL')
        self.token: str = self.get_item(config_data, 'HARDCOVER_API_TOKEN')
        self.db_url: str = "https://api.hardcover.app/v1/graphql"

        self.validate_folders()
        self.validate_index_files()


    def get_item(self, config_dict, config_key):
        return (
            config_dict[config_key]
            if isinstance(config_dict, dict) and len(config_dict.values()) > 0
            else False
        )


    def validate_folders(self):
        for x, y in self.default_folders.items():
            try:
                Path(y).mkdir(parents=True, exist_ok=True)
            except:
                ErrorModal(f"Can't make folder: {y}!")


    def validate_index_files(self):
        for x, y in self.index_file_dict.items():
            try:
                if not Path(y).exists():
                    Path(y).write_text("")
            except:
                ErrorModal(f"Can't make Index file: {y}")


    def config_check(self):
        full_path=f"{self.path}/.config"
        if Path(full_path).is_file():
            return self.read_config(full_path)
        else:
            Path(full_path).write_text("")
            return False


    def read_config(self, full_path):
        try:
            with open(full_path) as config_json:
                return json.load(fp=config_json)
        except:
            return False
