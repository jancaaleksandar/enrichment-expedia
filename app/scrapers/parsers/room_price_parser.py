import json
from typing import Dict, List, TypedDict

from ...db.models import LeadHotelRunModel
from ..types.room import (
    ExtraDetails,
    OfferDetails,
    PriceDetails,
    RefundableDetails,
    RoomDetails,
)
from ..utils.common.construct_url import contruct_url


class RoomPriceParserResponseType(TypedDict):
    successfully_parsed: bool
    offer_details: List[RoomDetails]


class RoomPriceParser:
    def __init__(
        self, response: dict, params: LeadHotelRunModel, competitor_data_id: int
    ):
        self.response = response
        self.params = params
        self.competitor_data_id = competitor_data_id
        with open("debug/response.json", "w") as f:
            json.dump(response, f, indent=4)

    def _get_categorized_listings(self) -> List[Dict[any, any]]:
        print(f"DEBUG: response structure: {type(self.response)}")
        response_data = self.response.get("response", None)
        print(f"DEBUG: response_data type: {type(response_data)}")

        if response_data is None:
            raise Exception("Response data is None")

        data_block = response_data.get("data", {})
        print(f"DEBUG: data_block type: {type(data_block)}")

        with open("debug/data_block.json", "w") as f:
            json.dump(data_block, f, indent=4)
        if not data_block:
            raise Exception("No data block found")

        property_offers = data_block.get("propertyOffers", {})
        print(f"DEBUG: property_offers type: {type(property_offers)}")
        if not property_offers:
            raise Exception("No property offers found")

        categorized_listings = property_offers.get("categorizedListings", [])
        print(
            f"DEBUG: categorized_listings type: {type(categorized_listings)}, length: {len(categorized_listings) if categorized_listings else 'None'}"
        )
        if not categorized_listings:
            raise Exception("No categorized listings found")

        return categorized_listings

    def _check_if_room_is_sold_out(self, property_unit: Dict[any, any]) -> bool:
        availability_cta = property_unit.get("availabilityCallToAction", {})
        if availability_cta:
            availability_message = availability_cta.get("value", None)
            if (
                availability_message
                and availability_message.strip() == "We are sold out"
            ):
                return True
        return False

    def _find_matching_selections(
        self, secondary_selections: Dict[any, any], rate_plan_id: str
    ) -> Dict[any, any]:
        for selection in secondary_selections:
            secondary_selection = selection.get("secondarySelection", None)
            if (
                secondary_selection
                and secondary_selection.get("id", None) == rate_plan_id
            ):
                return selection

            tertiary_selections = selection.get("tertiarySelections", [])
            if tertiary_selections:
                for tertiary_selection in tertiary_selections:
                    if tertiary_selection.get("optionId", None) == rate_plan_id:
                        return tertiary_selection
        return None

    def _get_extras(
        self, matched_secondary_selection: Dict[any, any], rate_plan_id: str
    ) -> List[ExtraDetails]:
        extra_details: List[ExtraDetails] = []
        tertiary_selections = matched_secondary_selection.get("tertiarySelections", [])
        if tertiary_selections:
            for tertiary in tertiary_selections:
                if (
                    tertiary.get("optionId", None) == rate_plan_id
                    and tertiary.get("description") != "No extras"
                ):
                    extra_details.append(
                        ExtraDetails(
                            extra_details_description=tertiary.get("description"),
                            extra_details_price=tertiary.get("price"),
                        )
                    )
        return extra_details

    def _get_clean_price(self, price_str: str) -> float:
        cleaned = (
            price_str.replace("$", "")
            .replace("€", "")
            .replace("\u20ac", "")
            .replace("£", "")
            .replace("\u00a3", "")
            .replace("total", "")
            .replace("per night", "")
            .replace("+", "")
            .replace(",", "")
            .strip()
        )
        return float(cleaned)

    def _get_total_price(self, display_messages: List[Dict[any, any]]) -> float:
        total_price = None
        for message in display_messages:
            if message.get("role", None) == "TOTAL":
                formatted_price = message.get("formatted", None)
                if formatted_price:
                    total_price = self._get_clean_price(price_str=formatted_price)
            line_items = message.get("lineItems", [])
            if not line_items:
                raise Exception("No line items found")

            for item in line_items:
                if (
                    item.get("__typename", None) == "DisplayPrice"
                    and item.get("role", None) == "LEAD"
                    and item.get("price", {}).get("formatted", None)
                ):
                    total_price = self._get_clean_price(
                        price_str=item.get("price", {}).get("formatted", None)
                    )

        return total_price

    def _parse_price_details(self, rate_plan: Dict[any, any]) -> PriceDetails:
        price_details = rate_plan.get("priceDetails", [])
        if not price_details:
            raise Exception("No price details found")

        price_block = price_details[0].get("price", {})
        if not price_block:
            raise Exception("No price block found")

        display_messages = price_block.get("displayMessages", [])
        if not display_messages:
            raise Exception("No display messages found")

        total_price = self._get_total_price(display_messages=display_messages)
        if total_price is None:
            raise Exception("No total price found")

        night_price = total_price / self.params.lead_hotel_run_request_length_of_stay

        return PriceDetails(
            price_details_night_price=night_price, price_details_total_price=total_price
        )

    def _get_refundable_info_with_secondary_selection(
        self,
        matched_secondary_selection: Dict[any, any],
        refundable_content: Dict[any, any],
    ) -> RefundableDetails:
        refundable_description = "Non-refundable"

        if isinstance(matched_secondary_selection.get("secondarySelection"), dict):
            refundable_description = matched_secondary_selection[
                "secondarySelection"
            ].get("description", refundable_description)
        elif (
            refundable_content
            and isinstance(refundable_content.get("messages"), list)
            and len(refundable_content["messages"]) > 0
        ):
            first_message = refundable_content["messages"][0]
            if isinstance(first_message, dict):
                refundable_description = first_message.get(
                    "text", refundable_description
                )

        refundable = (
            isinstance(refundable_description, str)
            and "refundable" in refundable_description.lower()
            and "non-refundable" not in refundable_description.lower()
        )

        return RefundableDetails(
            refundable_details_refundable=refundable,
            refundable_details_refundable_description=refundable_description,
        )

    def _get_refundable_info_no_secondary_selection(
        self, refundable_content: Dict[any, any]
    ) -> RefundableDetails:
        refundable_description = "Non-refundable"
        refundable = False
        messages = refundable_content.get("messages", [])
        if messages:
            for message in messages:
                if "refundable" in message.get("text", "").lower():
                    refundable = True
                    refundable_description = message.get("text", "")
                    break

        return RefundableDetails(
            refundable_details_refundable=refundable,
            refundable_details_refundable_description=refundable_description,
        )

    def _parse_offers(self, primary_selections: Dict[any, any]) -> OfferDetails:
        offer_details: List[OfferDetails] = []
        refundable_details: RefundableDetails = {
            "refundable_details_refundable": False,
        }
        price_details: PriceDetails = {
            "price_details_night_price": None,
            "price_details_total_price": None,
        }
        extras: List[ExtraDetails] = []

        with open("debug/primary_selections.json", "w") as f:
            json.dump(primary_selections, f, indent=4)

        for selection in primary_selections:
            rate_plans = selection.get("ratePlans", [])
            secondary_selections = selection.get("secondarySelections", [])

            for plan in rate_plans:
                reserve_cta = plan.get("reserveCallToAction", {})
                refundable_content = reserve_cta.get("content", {})

                if secondary_selections:
                    rate_plan_id = plan.get("id", None)
                    if not rate_plan_id:
                        continue

                    matched_secondary_selection = self._find_matching_selections(
                        secondary_selections=secondary_selections,
                        rate_plan_id=rate_plan_id,
                    )
                    if not matched_secondary_selection:
                        continue

                    refundable_details = (
                        self._get_refundable_info_with_secondary_selection(
                            matched_secondary_selection=matched_secondary_selection,
                            refundable_content=refundable_content,
                        )
                    )
                    extras = self._get_extras(
                        matched_secondary_selection=matched_secondary_selection,
                        rate_plan_id=rate_plan_id,
                    )
                    price_details = self._parse_price_details(rate_plan=plan)

                elif not secondary_selections:
                    price_details = self._parse_price_details(rate_plan=plan)
                    refundable_details = (
                        self._get_refundable_info_no_secondary_selection(
                            refundable_content=refundable_content
                        )
                    )
                    extras = None

                offer_details.append(
                    OfferDetails(
                        offer_details_refundable=refundable_details[
                            "refundable_details_refundable"
                        ],
                        offer_details_refundable_description=refundable_details[
                            "refundable_details_refundable_description"
                        ],
                        offer_details_price_night=price_details[
                            "price_details_night_price"
                        ],
                        offer_details_price_total=price_details[
                            "price_details_total_price"
                        ],
                        offer_details_extras=extras,
                    )
                )
        return offer_details

    def _get_room_details(self, room: Dict[any, any]) -> RoomDetails:
        features_block = room.get("features", None)
        print(
            f"DEBUG: features_block type: {type(features_block)}, value: {features_block}"
        )

        guests = None  # * change this for main expedia
        if features_block is None:
            print("WARNING: features_block is None, returning default room details")
            return RoomDetails(room_details_guests=guests)

        for feature in features_block:
            print(f"DEBUG: Processing feature: {feature}")
            graphic = feature.get("graphic", {})
            print(f"DEBUG: graphic: {graphic}")
            # Updated to handle the actual structure where graphic has direct 'id' field
            if graphic and graphic.get("id") == "people":
                guests = feature.get("text", None)
                print(f"DEBUG: Found guests info: {guests}")
                break

        return RoomDetails(room_details_guests=guests)

    def parse(self) -> RoomPriceParserResponseType:
        successfully_parsed = False
        offer_details: List[OfferDetails] = []

        try:
            categorized_listings = self._get_categorized_listings()
            url = contruct_url(params=self.params)

            for i, room in enumerate(categorized_listings):
                print(f"DEBUG: Processing room {i}: {type(room)}")
                primary_selections = room.get("primarySelections", [])
                print(
                    f"DEBUG: primary_selections type: {type(primary_selections)}, length: {len(primary_selections) if primary_selections else 'None'}"
                )
                if not primary_selections:
                    print(f"DEBUG: Skipping room {i} - no primary selections")
                    continue

                print(f"DEBUG: Calling _get_room_details for room {i}")
                room_details = self._get_room_details(room=room)
                print(f"DEBUG: Got room_details: {room_details}")

                property_unit = primary_selections[0].get("propertyUnit", {})
                print(f"DEBUG: property_unit type: {type(property_unit)}")
                sold_out = self._check_if_room_is_sold_out(property_unit=property_unit)
                print(f"DEBUG: sold_out: {sold_out}")

                header = room.get("header", {})
                print(f"DEBUG: header type: {type(header)}, value: {header}")
                # Try both 'title' and 'text' fields for room name
                room_name = None
                if header:
                    room_name = header.get("title", None) or header.get("text", None)
                print(f"DEBUG: room_name: {room_name}")
                if not room_name:
                    raise Exception("No room name found")

                if not sold_out:
                    offers = self._parse_offers(primary_selections=primary_selections)
                    if not offers:
                        raise Exception("No offers found")

                for offer in offers:
                    offer_details.append(
                        RoomDetails(
                            room_details_name=room_name,
                            room_details_guests=room_details["room_details_guests"],
                            room_details_sold_out=sold_out,
                            offer_details_price_night=offer[
                                "offer_details_price_night"
                            ],
                            offer_details_price_total=offer[
                                "offer_details_price_total"
                            ],
                            offer_details_refundable=offer["offer_details_refundable"],
                            offer_details_refundable_description=offer[
                                "offer_details_refundable_description"
                            ],
                            offer_details_extras=offer["offer_details_extras"],
                            offer_details_url=url,
                            offer_details_competitor_data_id=self.competitor_data_id,
                        )
                    )

            successfully_parsed = True

        except Exception as e:
            print(f"Error parsing price: {e}")
            successfully_parsed = False

        return RoomPriceParserResponseType(
            successfully_parsed=successfully_parsed, offer_details=offer_details
        )
