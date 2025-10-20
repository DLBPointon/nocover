from nocover.config import Config

from nocover.hardcover.get_data import GetData


class ListData(GetData):
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        super().__init__(query, api_path, config_path, offline)

        self.slugs: list[str] = self.get_list_slugs()
        self.lists = self.reformat_data_by_dict()


    def reformat_data_by_dict(self):
        """
        Reformat the list data into something more sensible
        """
        organised_dict = {}

        for list_slug in self.slugs:
            list_data = next(data for data in self.data if data["slug"] == list_slug)

            organised_dict[list_slug] = {
                "list_information" : {
                    "slug": list_slug,
                    "name": list_data["name"],
                    "description": list_data["description"],
                    "like_count": list_data["likes_count"],
                    "follower_count": list_data["followers_count"],
                    "last_updated": list_data["updated_at"],
                    "book_count": list_data["books_count"]
                },
                "book_list": self.corrected_book_list(list_data["list_books"])
            }

        return organised_dict
