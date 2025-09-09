import json
from datetime import datetime
from typing import cast

from ...db.models import LeadHotelRunModel
from ..types.http import RequestParameters
from ..utils.common.common_calculate_check_out_date import calculate_check_out_date
from ..utils.common.common_date_to_dict import date_to_dict


def get_price_configuration(params: LeadHotelRunModel) -> RequestParameters:
    check_out_date_calulcated = calculate_check_out_date(
        cast("datetime", params.lead_hotel_run_request_check_in_date),
        cast("int", params.lead_hotel_run_request_length_of_stay),
    )
    check_in_date = date_to_dict(
        cast(datetime, params.lead_hotel_run_request_check_in_date)
    )
    check_out_date = date_to_dict(check_out_date_calulcated)
    request_type = "POST"
    url = "https://euro.expedia.net/graphql"
    request_cookies = None
    request_body = json.dumps(
        {
            "operationName": "RoomsAndRatesPropertyOffersQuery",
            "variables": {
                "propertyId": params.lead_hotel_run_request_provider_id,
                "searchCriteria": {
                    "primary": {
                        "dateRange": {
                            "checkInDate": {
                                "day": check_in_date["day"],
                                "month": check_in_date["month"],
                                "year": check_in_date["year"],
                            },
                            "checkOutDate": {
                                "day": check_out_date["day"],
                                "month": check_out_date["month"],
                                "year": check_out_date["year"],
                            },
                        },
                        "destination": {
                            "regionName": None,
                            "regionId": None,
                            "coordinates": None,
                            "pinnedPropertyId": None,
                            "propertyIds": None,
                            "mapBounds": None,
                        },
                        "rooms": [{"adults": 2, "children": []}],
                    },
                    "secondary": {
                        "counts": [],
                        "booleans": [],
                        "selections": [
                            {"id": "privacyTrackingState", "value": "CAN_NOT_TRACK"},
                            {
                                "id": "searchId",
                                "value": "be32e279-5b6f-4839-9ed6-b4f90a7024ea",
                            },
                            {"id": "sort", "value": "RECOMMENDED"},
                            {"id": "useRewards", "value": "SHOP_WITHOUT_POINTS"},
                        ],
                        "ranges": [],
                    },
                },
                "shoppingContext": {"multiItem": None},
                "travelAdTrackingInfo": None,
                "context": {
                    "siteId": 4400,
                    "locale": "en_IE",
                    "eapid": 400,
                    "tpid": 63,
                    "currency": "EUR",
                    "device": {"type": "DESKTOP"},
                    "identity": {
                        "duaid": "bf2e8fd7-9639-4627-a771-4bf5f3333eb5",
                        "authState": "ANONYMOUS",
                    },
                    "privacyTrackingState": "CAN_NOT_TRACK",
                    "debugContext": {"abacusOverrides": []},
                },
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "0c29b592f89c56e3ca69b787f406b01163a6fcb19c014cd71d7559fd72139704",
                }
            },
        }
    )
    request_headers = {
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
        "TE": "trailers",
    }

    return RequestParameters(
        request_type=request_type,
        url=url,
        request_proxy="",  # will be set by executor
        request_cookies=request_cookies,
        request_body=request_body,
        request_headers=request_headers,
    )
