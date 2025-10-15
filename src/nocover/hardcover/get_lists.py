import json
from nocover.config import Config

from nocover.hardcover.get_data import GetData

from nocover.general_functions import get_remote_data, json_dump

class ListData(GetData):
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        super().__init__(query, api_path, config_path, offline)

        self.slugs: list[str] = self.get_list_slugs()
        self.lists = self.reformat_data_by_dict()


    def reorder_by_list_position(self, books):
        return sorted(
                        books,
                        key=lambda x: x["list_position"],
                        reverse=False
                    )


    def corrected_book(self, book):
        data = book["book"]
        return {
            "list_position": book["position"],
            "book_title": data["title"],
            "book_series": [ i["series"]["slug"] for i in data["book_series"] ],
            "book_description": data["description"].encode().decode('unicode-escape'),
            "book_pages": data["pages"],
            "book_hc_creation": data["created_at"],
            "book_cover": data["image"]["url"],
            "book_ratings": data["rating"],
            "book_ratings_count": data["ratings_count"],
            "book_review_count": data["reviews_count"],
            "book_release_data": data["release_date"],
            "book_state": data["state"],
            "book_read_count": data["users_read_count"],
            "book_tags": self.format_tags([ i["tag"]["tag"] for i in data["taggings"]])
        }


    def corrected_book_list(self, book_list):
        return self.reorder_by_list_position(
            [
                self.corrected_book(i) for i in book_list
            ]
        )


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
