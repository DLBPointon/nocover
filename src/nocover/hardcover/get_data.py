import json

from nocover.config import Config

from nocover.general_functions import get_remote_data

from nocover.modals.error_page import ErrorModal


class GetData:
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        self.query: str          = query
        self.db_url: str         = config_path.db_url
        self.config: Config      = config_path
        self.offline: bool       = offline
        get_data: Any       = ( #ty: ignore[unresolved-reference]
            # Stuff for offline data handling would go here
            get_remote_data(query=query, token=self.config.token, url=self.db_url)
        )
        allowed_api_paths = ["lists", "user_books"]
        if not api_path in ["lists", "user_books", "profile"]:
            ErrorModal(f"Dev made an error, they used {api_path} where only one the below is allowed:\n{allowed_api_paths}")

        # Profile data is processed differently
        self.data = ( get_data["me"][0] if api_path == "profile" else get_data["me"][0][api_path] )


    def format_tags(self, data):
        """
        format a long list of tags into a new line seperated list
        """
        return "\n".join(list(set(data)))

    def get_list_slugs(self):
        """
        Get the top level slug from the data
        We can think of these as series names so that data such as {"list_1":["book_1", "book_2"]}
        """
        return [ i["slug"] for i in self.data ]
