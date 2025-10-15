from nocover.brl.book import Book

class ListBook(Book):
    def __init__(self, book_dict, *args, **kwargs):
        super().__init__(book_dict, *args, **kwargs)
        release_data: str = book_dict["book"]["release_date"]
        self.release_year       = (
            "0000" if release_data is None else release_data.split("-")[0]
        )
        self.book_publisher: str = self.get_publisher(book_dict["book"].get("publisher", None))
        self.book_isbn13: str = self.get_isbn13(book_dict["book"].get("isbn_13", None))
