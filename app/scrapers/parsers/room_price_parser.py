from typing import TypedDict, cast

from ...db.models import LeadHotelRunModel
from ..types.room import ExtraDetails, PriceDetails, RefundableDetails, RoomDetails
from ..utils.common.construct_url import contruct_url


class RoomPriceParserResponseType(TypedDict):
    successfully_parsed: bool
    offer_details: list[RoomDetails]


class RoomPriceParser:
    def __init__(
        self,
        response: dict[str, object],
        params: LeadHotelRunModel,
        competitor_data_id: int,
    ):
        self.response = response
        self.params = params
        self.competitor_data_id = competitor_data_id
        # with open("debug/response.json", "w") as f:
        #     json.dump(response, f, indent=4)

    def _get_categorized_listings(self) -> list[dict[str, object]]:
        print(f"DEBUG: response structure: {type(self.response)}")
        response_data = self.response.get("response", None)
        print(f"DEBUG: response_data type: {type(response_data)}")

        if response_data is None:
            raise ValueError("Response data is None")

        data_block = cast(
            dict[str, object], cast(dict[str, object], response_data).get("data", {})
        )
        print(f"DEBUG: data_block type: {type(data_block)}")

        # with open("debug/data_block.json", "w") as f:
        #     json.dump(data_block, f, indent=4)
        if not data_block:
            raise ValueError("No data block found")

        property_offers = cast(dict[str, object], data_block.get("propertyOffers", {}))
        print(f"DEBUG: property_offers type: {type(property_offers)}")
        if not property_offers:
            raise ValueError("No property offers found")

        categorized_listings = cast(
            list[dict[str, object]], property_offers.get("categorizedListings", [])
        )
        print(
            f"DEBUG: categorized_listings type: {type(categorized_listings)}, length: {len(categorized_listings) if categorized_listings else 'None'}"
        )
        if not categorized_listings:
            raise ValueError("No categorized listings found")

        return categorized_listings

    def _check_if_room_is_sold_out(self, property_unit: dict[str, object]) -> bool:
        availability_cta = cast(
            dict[str, object], property_unit.get("availabilityCallToAction", {})
        )
        if availability_cta:
            availability_message: str | None = (
                cast(str, availability_cta.get("value"))
                if availability_cta.get("value") is not None
                else None
            )
            if (
                availability_message
                and availability_message.strip() == "We are sold out"
            ):
                return True
        return False

    def _find_matching_selections(
        self, secondary_selections: dict[str, object], rate_plan_id: str
    ) -> dict[str, object]:
        for selection in secondary_selections:
            secondary_selection = cast(dict[str, object], selection).get(
                "secondarySelection", None
            )
            if (
                secondary_selection
                and cast(dict[str, object], secondary_selection).get("id", None)
                == rate_plan_id
            ):
                return cast(dict[str, object], selection)

            tertiary_selections = cast(dict[str, object], selection).get(
                "tertiarySelections", []
            )
            if tertiary_selections:
                for tertiary_selection in cast(
                    list[dict[str, object]], tertiary_selections
                ):
                    if tertiary_selection.get("optionId", None) == rate_plan_id:
                        return tertiary_selection
        return {}

    def _get_extras(
        self, matched_secondary_selection: dict[str, object], rate_plan_id: str
    ) -> list[ExtraDetails]:
        extra_details: list[ExtraDetails] = []
        tertiary_selections = matched_secondary_selection.get("tertiarySelections", [])
        if tertiary_selections:
            extra_details.extend(
                [
                    ExtraDetails(
                        extra_details_description=cast(
                            str, tertiary.get("description", "")
                        ),
                        extra_details_price=cast(float, tertiary.get("price", 0.0)),
                    )
                    for tertiary in cast(list[dict[str, object]], tertiary_selections)
                    if tertiary.get("optionId", None) == rate_plan_id
                    and tertiary.get("description") != "No extras"
                ]
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

    def _get_total_price(self, display_messages: list[dict[str, object]]) -> float:
        total_price = None
        for message in display_messages:
            if message.get("role", None) == "TOTAL":
                formatted_price = message.get("formatted", None)
                if formatted_price:
                    total_price = self._get_clean_price(
                        price_str=cast(str, formatted_price)
                    )
            line_items = message.get("lineItems", [])
            if not line_items:
                raise ValueError("No line items found")

            for item in cast(list[dict[str, object]], line_items):
                if (
                    item.get("__typename", None) == "DisplayPrice"
                    and item.get("role", None) == "LEAD"
                    and cast(dict[str, object], item.get("price", {})).get(
                        "formatted", None
                    )
                ):
                    price_dict = cast(dict[str, object], item.get("price", {}))
                    total_price = self._get_clean_price(
                        price_str=cast(str, price_dict.get("formatted", ""))
                    )

        return total_price if total_price is not None else 0.0

    def _parse_price_details(self, rate_plan: dict[str, object]) -> PriceDetails:
        price_details = rate_plan.get("priceDetails", [])
        if not price_details:
            raise ValueError("No price details found")

        price_block = (
            cast(
                dict[str, object],
                cast(dict[str, object], cast(list[dict[str, object]], price_details)[0]).get("price", {}),  # type: ignore
            )
            if price_details
            else {}
        )
        if not price_block:
            raise ValueError("No price block found")

        display_messages = price_block.get("displayMessages", [])
        if not display_messages:
            raise ValueError("No display messages found")

        total_price = self._get_total_price(
            display_messages=cast(list[dict[str, object]], display_messages)
        )

        night_price = (
            float(total_price)
            / self.params.lead_hotel_run_request_length_of_stay.get_value()
        )

        return PriceDetails(
            price_details_night_price=night_price, price_details_total_price=total_price
        )

    def _get_refundable_info_with_secondary_selection(
        self,
        matched_secondary_selection: dict[str, object],
        refundable_content: dict[str, object],
    ) -> RefundableDetails:
        refundable_description = "Non-refundable"

        if isinstance(matched_secondary_selection.get("secondarySelection"), dict):
            refundable_description = cast(
                dict[str, object], matched_secondary_selection["secondarySelection"]
            ).get("description", refundable_description)
        elif (
            refundable_content
            and isinstance(refundable_content.get("messages"), list)
            and len(cast(list[dict[str, object]], refundable_content["messages"])) > 0
        ):
            messages = cast(list[dict[str, object]], refundable_content["messages"])
            first_message = messages[0]
            refundable_description = first_message.get("text", refundable_description)

        refundable = (
            isinstance(refundable_description, str)
            and "refundable" in refundable_description.lower()
            and "non-refundable" not in refundable_description.lower()
        )

        return RefundableDetails(
            refundable_details_refundable=refundable,
            refundable_details_refundable_description=cast(str, refundable_description),
        )

    def _get_refundable_info_no_secondary_selection(
        self, refundable_content: dict[str, object]
    ) -> RefundableDetails:
        refundable_description = "Non-refundable"
        refundable = False
        messages = cast(list[dict[str, object]], refundable_content.get("messages", []))
        if messages:
            for message in messages:
                if "refundable" in cast(str, message.get("text", "")).lower():
                    refundable = True
                    refundable_description = cast(str, message.get("text", ""))
                    break

        return RefundableDetails(
            refundable_details_refundable=refundable,
            refundable_details_refundable_description=refundable_description,
        )

    def _parse_offers(
        self, primary_selections: list[dict[str, object]]
    ) -> list[RoomDetails]:
        offer_details: list[RoomDetails] = []
        refundable_details: RefundableDetails = {
            "refundable_details_refundable": False,
            "refundable_details_refundable_description": "Non-refundable",
        }
        price_details: PriceDetails = {
            "price_details_night_price": None,
            "price_details_total_price": None,
        }
        extras: list[ExtraDetails] = []

        # with open("debug/primary_selections.json", "w") as f:
        #     json.dump(primary_selections, f, indent=4)

        for selection in primary_selections:
            rate_plans = selection.get("ratePlans", [])
            secondary_selections = selection.get("secondarySelections", [])

            for plan in cast(list[dict[str, object]], rate_plans):
                reserve_cta = cast(
                    dict[str, object], plan.get("reserveCallToAction", {})
                )
                refundable_content = cast(
                    dict[str, object], reserve_cta.get("content", {})
                )

                if secondary_selections:
                    rate_plan_id = plan.get("id", None)
                    if not rate_plan_id:
                        continue

                    matched_secondary_selection = self._find_matching_selections(
                        secondary_selections=cast(
                            dict[str, object], secondary_selections
                        ),
                        rate_plan_id=cast(str, rate_plan_id),
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
                        rate_plan_id=cast(str, rate_plan_id),
                    )
                    price_details = self._parse_price_details(rate_plan=plan)

                elif not secondary_selections:
                    price_details = self._parse_price_details(rate_plan=plan)
                    refundable_details = (
                        self._get_refundable_info_no_secondary_selection(
                            refundable_content=refundable_content
                        )
                    )
                    extras: list[ExtraDetails] = []

                offer_details.append(
                    RoomDetails(
                        room_details_name="Unknown",
                        room_details_guests=0,
                        room_details_sold_out=False,
                        offer_details_refundable=refundable_details[
                            "refundable_details_refundable"
                        ],
                        offer_details_refundable_description=refundable_details[
                            "refundable_details_refundable_description"
                        ],
                        offer_details_price_night=cast(
                            float, price_details["price_details_night_price"]
                        ),
                        offer_details_price_total=cast(
                            float, price_details["price_details_total_price"]
                        ),
                        offer_details_extras=extras,
                        offer_details_url="",
                        offer_details_competitor_data_id=self.competitor_data_id,
                    )
                )
        return offer_details

    def _get_room_details(self, room: dict[str, object]) -> RoomDetails:
        features_block = room.get("features", None)
        print(
            f"DEBUG: features_block type: {type(features_block)}, value: {features_block}"
        )

        guests: int = 0  # * change this for main expedia
        if features_block is None:
            print("WARNING: features_block is None, returning default room details")
            return RoomDetails(
                room_details_name="Unknown",
                room_details_guests=0,
                room_details_sold_out=True,
                offer_details_price_night=0.0,
                offer_details_price_total=0.0,
                offer_details_refundable=False,
                offer_details_refundable_description="",
                offer_details_extras=None,
                offer_details_url="",
                offer_details_competitor_data_id=self.competitor_data_id,
            )

        for feature in cast(list[dict[str, object]], features_block):
            print(f"DEBUG: Processing feature: {feature}")
            graphic = feature.get("graphic", {})
            print(f"DEBUG: graphic: {graphic}")
            # Updated to handle the actual structure where graphic has direct 'id' field
            if graphic and cast(dict[str, object], graphic).get("id") == "people":
                guests = int(cast(str, feature.get("text", "0")))
                print(f"DEBUG: Found guests info: {guests}")
                break

        return RoomDetails(
            room_details_name="Unknown",
            room_details_guests=0,
            room_details_sold_out=True,
            offer_details_price_night=0.0,
            offer_details_price_total=0.0,
            offer_details_refundable=False,
            offer_details_refundable_description="",
            offer_details_extras=None,
            offer_details_url="",
            offer_details_competitor_data_id=self.competitor_data_id,
        )

    def parse(self) -> RoomPriceParserResponseType:
        successfully_parsed = False
        offer_details: list[RoomDetails] = []

        try:
            categorized_listings = self._get_categorized_listings()
            url = contruct_url(params=self.params)

            for i, room in enumerate(categorized_listings):
                print(f"DEBUG: Processing room {i}: {type(room)}")
                primary_selections = cast(
                    list[dict[str, object]],
                    (
                        room.get("primarySelections", [])
                        if isinstance(room.get("primarySelections"), list)
                        else []
                    ),
                )
                print(
                    f"DEBUG: primary_selections type: {type(primary_selections)}, length: {len(primary_selections) if primary_selections else 'None'}"
                )
                if not primary_selections:
                    print(f"DEBUG: Skipping room {i} - no primary selections")
                    continue

                print(f"DEBUG: Calling _get_room_details for room {i}")
                room_details = self._get_room_details(room=room)
                print(f"DEBUG: Got room_details: {room_details}")

                property_unit = cast(
                    dict[str, object], primary_selections[0].get("propertyUnit", {})
                )
                print(f"DEBUG: property_unit type: {type(property_unit)}")
                sold_out = self._check_if_room_is_sold_out(property_unit=property_unit)
                print(f"DEBUG: sold_out: {sold_out}")

                header = cast(dict[str, object], room.get("header", {}))
                print(f"DEBUG: header type: {type(header)}, value: {header}")
                # Try both 'title' and 'text' fields for room name
                room_name = None
                if header:
                    room_name = header.get("title", None) or header.get("text", None)
                print(f"DEBUG: room_name: {room_name}")
                if not room_name:
                    raise ValueError("No room name found")

                offers: list[RoomDetails] = []
                if not sold_out:
                    offers = self._parse_offers(primary_selections=primary_selections)
                    if not offers:
                        raise ValueError("No offers found")

                offer_details.extend(
                    [
                        RoomDetails(
                            room_details_name=cast(str, room_name),
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
                        for offer in offers
                    ]
                )

            successfully_parsed = True

        except (ValueError, KeyError, TypeError) as e:
            print(f"Error parsing price: {e}")
            successfully_parsed = False

        return RoomPriceParserResponseType(
            successfully_parsed=successfully_parsed, offer_details=offer_details
        )
