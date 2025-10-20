import json
from typing import Any
import xmltodict


class SeriesBrlData:
    """
    Reads data from brl file to populate Details Panel
    """

    def __init__(self, brl: str) -> None:
        self.series_brl_path = brl.strip()  # NO NEWLINES
        self.series_data = self.read_brl()

        series_data = self.series_data["Series"]
        self.series_name = series_data.get("@Name", "Unknown Series")

        self.series_description = str(series_data["Description"])

        self.universe_data = series_data.get("Universe", "Series is a standalone!")

        self.universe = self.make_universe_line()

        self.database_info = series_data["Database"]

        self.books = self.series_data["Books"]["Book"]

    def make_universe_line(self) -> str:
        return (
            f"Series belongs to the {self.universe_data['@Name']} Universe {
                (
                    ''
                    if self.universe_data['@Position'] is None
                    else f'(Position: {self.universe_data["@Position"]})'
                )
            }"
            if self.universe_data != "Series is a standalone!"
            else self.universe_data
        )

    def read_brl(self) -> Any:
        """
        Reads data from brl file to populate Details Panel
        """
        with open(self.series_brl_path) as xml_file:
            data_dict = xmltodict.parse(xml_file.read())

            json_data = json.dumps(data_dict)

            with open("data.json", "w") as json_file:
                json_file.write(json_data)

        return json.loads(json_data)["opml"]["ReadingList"]
