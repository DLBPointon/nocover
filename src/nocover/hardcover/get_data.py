
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
        allowed_api_paths = ["lists", "user_books", "prompts"]
        if api_path not in ["lists", "user_books", "profile", "prompts"]:
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
                    "name": list_data.get("name", list_data["question"]), # Fall back is when prompts are being used.
                    "description": list_data["description"],
                    "like_count": list_data.get("likes_count", "NA"),
                    "follower_count": list_data.get("followers_count", "NA"),
                    "last_updated": list_data.get("updated_at", "NA"),
                    "book_count": list_data["books_count"]
                },
                "book_list": self.corrected_book_list(list_data.get("list_books", list_data["prompt_books"]))
            }

        return organised_dict


    def corrected_book(self, book):
        data = book["book"]
        return {
            "list_position": book.get("position", "0"),
            "book_title": data["title"],
            "book_series": [ i["series"]["slug"] for i in data["book_series"] ],
            "book_description": data["description"].encode().decode('unicode-escape') if data["description"] is not None else None,
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


    def reorder_by_list_position(self, books):
        position_data = books[0].get("list_position", False)

        if position_data is False:
            return books
        else:
            return sorted(
                            books,
                            key=lambda x: x["list_position"],
                            reverse=False
                        )


    def corrected_book_list(self, book_list):
        return self.reorder_by_list_position(
            [
                self.corrected_book(i) for i in book_list
            ]
        )
