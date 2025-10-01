class Book:
    def __init__(self, book_dict):
        self.book_name          = book_dict["book"]["default_cover_edition"]["book"]["title"]
        self.book_slug          = book_dict["book"]["slug"]
        self.book_publisher     = self.get_publisher(book_dict)
        self.book_isbn13        = self.get_isbn13(book_dict)
        self.book_tags          = self.clean_book_tags(book_dict["book"]["taggings"])
        release_data: str       = book_dict["book"]["default_cover_edition"]["book"]["release_date"]
        self.release_year       = "0000" if release_data is None else release_data.split("-")[0]
        self.series_position    = 10000 if book_dict["position"] is None else book_dict["position"]
        self.series_pos_details = book_dict["details"]


    def get_publisher(self, data: dict) -> str:
        """
        Get publisher from dict if publisher != None
        """
        pub_name = data["book"]["default_cover_edition"]["publisher"]
        return (pub_name["name"] if pub_name is not None else "NA")


    def get_isbn13(self, data: dict) -> str:
        """
        Get isbn13 from dict if isbn_13 != None
        """
        isbn = data["book"]["default_cover_edition"]["isbn_13"]
        return (isbn if isbn is not None else "NA")


    def clean_book_tags(self, data: list) -> list:
        """
        Get unique list of tags from set of nested tags in tag data.
        """
        return list(set([ i["tag"]["tag"] for i in data ]))
