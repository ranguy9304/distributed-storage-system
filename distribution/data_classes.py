import json

class Data:
    def __init__(self, attributes, description):
        self.attributes = attributes
        self.desc = description

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_data):
        data_dict = json.loads(json_data)
        return Data(data_dict["attributes"], data_dict["desc"])