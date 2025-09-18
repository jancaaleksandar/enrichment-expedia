from typing import TypedDict, cast

from ..types.competitors import CompetitorParsedData


class CompetitorDetailsParserResponse(TypedDict):
    competitor_details_parsed: list[CompetitorParsedData]
    successfully_parsed: bool


class CompetitorDetailsParser:
    def __init__(self, response: dict[str, object]):
        self.response = response

    def _get_cards(self) -> list[dict[str, object]]:
        data_block = self.response.get("data", {})
        if not data_block:
            raise ValueError("No data block found")
        recommendations_module = cast(dict[str, object], data_block).get(
            "recommendationsModule", {}
        )
        if not recommendations_module:
            raise ValueError("No recommendations module found")

        cards_block = cast(dict[str, object], recommendations_module).get("cards", [])
        if not cards_block:
            raise ValueError("No cards block found")
        return cast(list[dict[str, object]], cards_block)

    def _parse_card(
        self, card: dict[str, object], position: int
    ) -> CompetitorParsedData:
        heading = card.get("heading", {})
        if not heading:
            raise ValueError("No heading found")
        hotel_name = cast(dict[str, object], heading).get("title", None)
        if not hotel_name:
            raise ValueError("No hotel name found")

        hotel_id = card.get("id", None)
        if not hotel_id:
            raise ValueError("No hotel id found")

        hotel_url = cast(
            dict[str, object],
            cast(dict[str, object], card.get("cardAction", {})).get("resource", {}),
        ).get("value", None)
        if not hotel_url:
            raise ValueError("No hotel url found")

        return CompetitorParsedData(
            competitor_parsed_data_hotel_id=cast(str, hotel_id),
            competitor_parsed_data_hotel_name=cast(str, hotel_name),
            competitor_parsed_data_hotel_url=cast(str, hotel_url),
            competitor_parsed_data_position=position,
        )

    def parse(self):
        successfully_parsed = False
        competitor_details_parsed: list[CompetitorParsedData] = []
        try:
            cards = self._get_cards()
            competitor_details_parsed.extend(
                [
                    self._parse_card(card=card, position=idx)
                    for idx, card in enumerate(cards)
                ]
            )
            successfully_parsed = True
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error parsing competitor details: {e}")
            successfully_parsed = False

        return CompetitorDetailsParserResponse(
            competitor_details_parsed=competitor_details_parsed,
            successfully_parsed=successfully_parsed,
        )
