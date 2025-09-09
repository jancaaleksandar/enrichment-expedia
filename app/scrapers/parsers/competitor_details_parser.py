from typing import Dict, List, TypedDict

from ..types.competitors import CompetitorParsedData


class CompetitorDetailsParserResponse(TypedDict):
    competitor_details_parsed: List[CompetitorParsedData]
    successfully_parsed: bool


class CompetitorDetailsParser:
    def __init__(self, response: dict):
        self.response = response

    def _get_cards(self) -> List[Dict[any, any]]:
        data_block = self.response.get("data", {})
        if not data_block:
            raise Exception("No data block found")
        recommendations_module = data_block.get("recommendationsModule", {})
        if not recommendations_module:
            raise Exception("No recommendations module found")

        cards_block = recommendations_module.get("cards", [])
        if not cards_block:
            raise Exception("No cards block found")
        return cards_block

    def _parse_card(self, card: Dict[any, any]) -> CompetitorParsedData:
        heading = card.get("heading", {})
        if not heading:
            raise Exception("No heading found")
        hotel_name = heading.get("title", None)
        if not hotel_name:
            raise Exception("No hotel name found")

        hotel_id = card.get("id", None)
        if not hotel_id:
            raise Exception("No hotel id found")

        hotel_url = card.get("cardAction", {}).get("resource", {}).get("value", None)
        if not hotel_url:
            raise Exception("No hotel url found")

        return CompetitorParsedData(
            competitor_parsed_data_hotel_id=hotel_id,
            competitor_parsed_data_hotel_name=hotel_name,
            competitor_parsed_data_hotel_url=hotel_url,
        )

    def parse(self):
        successfully_parsed = False
        competitor_details_parsed: List[CompetitorParsedData] = []
        try:
            cards = self._get_cards()
            for card in cards:
                competitor_details_parsed.append(self._parse_card(card=card))
            successfully_parsed = True
        except Exception as e:
            print(f"Error parsing competitor details: {e}")
            successfully_parsed = False

        return CompetitorDetailsParserResponse(
            competitor_details_parsed=competitor_details_parsed,
            successfully_parsed=successfully_parsed,
        )
