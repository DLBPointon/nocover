import json
import xmltodict

from nocover.config import Config
from nocover.general_functions import get_remote_data

class SeriesData:
    """
    Reads data from brl file to populate Details Panel
    """
    def __init__(
        self, brl: str
    ) -> None:
        self.series_brl_path    = brl.strip() # NO NEWLINES
        #self.series_body_data   = self.get_body()
        read_brl= self.read_brl()
        self.series_data        = read_brl

    def read_brl(self):
        with open(self.series_brl_path) as xml_file:

            data_dict = xmltodict.parse(xml_file.read())
            # xml_file.close()

            # generate the object using json.dumps()
            # corresponding to json data

            json_data = json.dumps(data_dict)

            # Write the json data to output
            # json file
            with open("data.json", "w") as json_file:
                json_file.write(json_data)

        return json.loads(json_data)['opml']['ReadingList']

    # def get_body(self):
    #     for x, y in self.series_head_data.items():
    #         brl_data = self.read_brl(y["series_brl"])
