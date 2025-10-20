from typing import Any


class Book:
    def __init__(self, book_dict):
        book_data = book_dict["book"]
        cover_edition = book_data.get("default_cover_edition", {}).get(
            "book", book_data
        )
        self.book_name = cover_edition.get("title", "Unknown Title")
        self.book_slug = book_data.get("slug")
        self.book_publisher = self.get_publisher(cover_edition.get("publisher", None))
        self.book_isbn13 = self.get_isbn13(cover_edition.get("isbn_13", None))
        self.book_tags = self.clean_book_tags(cover_edition["taggings"])
        release_data: str = cover_edition["release_date"]
        self.release_year = (
            "0000" if release_data is None else release_data.split("-")[0]
        )
        self.series_position = (
            10000 if book_dict.get("position", None) is None else book_dict["position"]
        )

        book_deets = book_dict.get("details", None)
        self.series_pos_details = "NA" if book_deets is None else book_deets

    def get_publisher(self, data: dict[str, Any]) -> str:
        """
        Get publisher from dict if publisher != None
        """
        return data["name"] if data is not None else "NA"

    def get_isbn13(self, data: str) -> str:
        """
        Get isbn13 from dict if isbn_13 != None
        """
        return data if data is not None else "NA"

    def clean_book_tags(self, data: list[dict[str, Any]]) -> list[str]:
        """
        Get unique list of tags from set of nested tags in tag data.
        """
        return list(set([i["tag"]["tag"] for i in data]))
