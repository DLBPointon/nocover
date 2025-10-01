from nocover.config import Config
from nocover.general_functions import get_remote_data

class Profile:
    def __init__(self, query: str, config_path: Config, offline: bool):
        self.query: str     = query
        self.db_url: str    = config_path.db_url
        self.config: Config = config_path
        self.offline: bool  = offline
        get_profile_data    = (
            # self.get_local_data(config_path)
            # if offline else
            get_remote_data(query=query, token=self.config.token, url=self.db_url)
        )
        data                = get_profile_data["me"][0]
        self.name: str      = data["name"]
        self.username: str  = data["username"]

        self.users_lists    = [x for x in data["lists"] ]
        self.followed_lists = [x.list.name for x in data["followed_lists"]]

        self.public_data_dict   = {
            "name":             self.name,
            "username":         self.username + f"(User# {data["id"]})",
            "email":            data["email"],
            "location":         data["location"],
            "birthdate":        data["birthdate"],
            "pronouns":         data["pronoun_personal"] + "/" + data["pronoun_possessive"],
            "account_created":  data["created_at"],
            "biography":        data["bio"]
        }

        self.book_data_dict     = {
            "book_count":       data["books_count"],
            "user_lists":       self.users_lists,
            "followed_lists":   self.followed_lists
        }

        self.private_data_dict  = {
            "membership_level":         data["membership"],
            "current_membership_ends":  data["membership_ends_at"],
            "access_level":             data["access_level"],
            "librarian_permissions":    data["librarian_roles"]
        }

    def save_data(self, data):
        """
        Save remote data
        """

    def get_local_data(self, config: str):
        """
        If offline get a local downloaded copy
        Saved from first online run
        """
        pass
