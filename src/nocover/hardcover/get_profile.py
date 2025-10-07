from nocover.config import Config

from nocover.hardcover.get_data import GetData

from nocover.general_functions import get_remote_data


class Profile(GetData):
    def __init__(self, query: str, api_path: str, config_path: Config, offline: bool):
        super().__init__(query, api_path, config_path, offline)

        self.name: str      = self.data["name"]
        self.username: str  = self.data["username"]

        self.users_lists    = [x for x in self.data["lists"] ]
        self.followed_lists = [x.list.name for x in self.data["followed_lists"]]

        self.public_data_dict   = {
            "name":             self.name,
            "username":         self.username + f"(User# {self.data["id"]})",
            "email":            self.data["email"],
            "location":         self.data["location"],
            "birthdate":        self.data["birthdate"],
            "pronouns":         self.data["pronoun_personal"] + "/" + self.data["pronoun_possessive"],
            "account_created":  self.data["created_at"],
            "biography":        self.data["bio"]
        }

        self.book_data_dict     = {
            "book_count":       self.data["books_count"],
            "user_lists":       self.users_lists,
            "followed_lists":   self.followed_lists
        }

        self.private_data_dict  = {
            "membership_level":         self.data["membership"],
            "current_membership_ends":  self.data["membership_ends_at"],
            "access_level":             self.data["access_level"],
            "librarian_permissions":    self.data["librarian_roles"]
        }
