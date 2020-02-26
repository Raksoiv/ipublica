import json


class APIParser:
    def parse_bidding(self, json_str: dict) -> dict:
        raise NotImplementedError

    def parse_day(self, json_str: dict) -> list:
        json_dict = json.loads(json_str)
        bidding_list = json_dict['Listado']
        bidding_id_list = []
        for bidding in bidding_list:
            bidding_id_list.append(bidding['CodigoExterno'])
        return bidding_id_list
