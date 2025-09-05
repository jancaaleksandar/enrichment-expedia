from datetime import datetime
from typing import cast
import json
from ..db.models import LeadHotelRunModel
from ..types.http import RequestParameters
from ..utils.common.common_calculate_check_out_date import calculate_check_out_date
from ..utils.common.common_date_to_dict import date_to_dict


def get_price_configuration(params : LeadHotelRunModel) -> RequestParameters:

    # IMPERSONATIONS = ["chrome133", "chrome132", "firefox135"]
    check_out_date_calulcated = calculate_check_out_date(cast("datetime", params.lead_hotel_run_request_check_in_date), cast("int", params.lead_hotel_run_request_length_of_stay))
    check_in_date = date_to_dict(cast("datetime", params.lead_hotel_run_request_check_in_date))
    check_out_date = date_to_dict(check_out_date_calulcated)

    currency_changeable_data = {
        "EUR": {
            "siteId": 4400,
            "locale": "en_IE",
            "eapid": 400,
            "tpid": 63,
            "url": "https://euro.expedia.net/graphql"
        },
        "USD": {
            "siteId": 1,
            "locale": "en_US",
            "eapid": 0,
            "tpid": 1,
            "url": "https://www.expedia.com/graphql"
        },
        "GBP": {
            "siteId": 3,
            "locale": "en_GB",
            "eapid": 0,
            "tpid": 3,
            "url": "https://www.expedia.co.uk/graphql"
        }
    }[params.lead_hotel_run_request_currency]

    # currency_changeable_data = {
    #     "siteId": 4400 if params["currency"] == "EUR" else 1,
    #     "locale": "en_IE" if params["currency"] == "EUR" else "en_US",
    #     "eapid": 400 if params["currency"] == "EUR" else 0,
    #     "tpid": 63 if params["currency"] == "EUR" else 1,
    #     "url": "https://euro.expedia.net/graphql" if params["currency"] == "EUR" else "https://www.expedia.com/graphql"
    # }

    return RequestParameters(
        request_type="POST",
        url=str(currency_changeable_data["url"]),
        request_proxy="",
        request_headers={
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "content-type": "application/json",
            "client-info": "shopping-pwa,78dcadebae7c41dfd3cc87c1859b7eaf495fcc92,us-east-1",
            "x-shopping-product-line": "lodging",
            "x-product-line": "lodging",
            "x-parent-brand-id": "expedia",
            "x-page-id": "page.Hotels.Infosite.Information,H,30",
            "x-hcom-origin-id": "page.Hotels.Infosite.Information,H,30",
            "Origin": "https://www.expedia.com",
            "Alt-Used": "www.expedia.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=4",
            "TE": "trailers"
        },
        request_cookies=None,
        request_body=str({  # type: ignore
            "operationName": "RoomsAndRatesPropertyOffersQuery",
            "variables": {
                "propertyId": params.task_hotel_provider_id,
                "searchCriteria": {
                    "primary": {
                        "dateRange": {
                            "checkInDate": check_in_date,
                            "checkOutDate": check_out_date
                        },
                        "destination": {
                            "regionName": None,
                            "regionId": None,
                            "coordinates": None,
                            "pinnedPropertyId": None,
                            "propertyIds": None,
                            "mapBounds": None
                        },
                        "rooms": [{"adults": 2, "children": []}]
                    },
                    "secondary": {
                        "counts": [],
                        "booleans": [],
                        "selections": [
                            {"id": "privacyTrackingState", "value": "CAN_NOT_TRACK"},
                            {"id": "searchId", "value": "be32e279-5b6f-4839-9ed6-b4f90a7024ea"},
                            {"id": "sort", "value": "RECOMMENDED"},
                            {"id": "useRewards", "value": "SHOP_WITHOUT_POINTS"}
                        ],
                        "ranges": []
                    }
                },
                "shoppingContext": {"multiItem": None},
                "travelAdTrackingInfo": None,
                "context": {
                    "siteId": currency_changeable_data["siteId"],
                    "locale": currency_changeable_data["locale"],
                    "eapid": currency_changeable_data["eapid"],
                    "tpid": currency_changeable_data["tpid"],
                    "currency": params.task__parsing_price_variables_currency,
                    "device": {"type": "DESKTOP"},
                    "identity": {
                        "duaid": "bf2e8fd7-9639-4627-a771-4bf5f3333eb5",
                        "authState": "ANONYMOUS"
                    },
                    "privacyTrackingState": "CAN_NOT_TRACK",
                    "debugContext": {"abacusOverrides": []}
                }
            }
        })),
