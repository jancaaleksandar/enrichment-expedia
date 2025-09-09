import json
from datetime import datetime
from typing import cast

from ...db.models import LeadHotelRunModel
from ..types.http import RequestParameters
from ..utils.common.common_calculate_check_out_date import calculate_check_out_date
from ..utils.common.common_date_to_dict import date_to_dict


def get_competitor_search_configuration(params: LeadHotelRunModel) -> RequestParameters:
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
            "operationName": "DiscoveryRecommendationsModuleQuery",
            "variables": {
                "contentSize": "LONG_FORM_FEATURED",
                "offeringType": "PRODUCT",
                "strategy": "ALTERNATIVE",
                "containerType": "CAROUSEL",
                "priceStrategy": "LIVE",
                "input": ["PRODUCT"],
                "recommendationContext": {
                    "outputLineOfBusiness": "LODGING",
                    "pageId": "HIS",
                    "lodging": {
                        "propertyId": params.lead_hotel_run_request_provider_id,
                        "checkin": check_in_date,
                        "checkout": check_out_date,
                        "rooms": [{"adults": 2, "children": []}],
                        "searchCriteria": {
                            "selections": [
                                {"id": "privacyTrackingState", "value": "CAN_TRACK"},
                                {
                                    "id": "selected",
                                    "value": params.lead_hotel_run_request_provider_id,
                                },
                                {"id": "sort", "value": "RECOMMENDED"},
                                {"id": "useRewards", "value": "SHOP_WITHOUT_POINTS"},
                            ]
                        },
                    },
                },
                "placementId": "142",
                "configurationIdentifier": "lodging_dated_pdp:lodging_highlights",
                "context": {
                    "siteId": 4400,
                    "locale": "en_IE",
                    "eapid": 400,
                    "tpid": 63,
                    "currency": "EUR",
                    "device": {"type": "DESKTOP"},
                    "identity": {
                        "duaid": "6a3f85e8-ad3e-4cec-8a74-8b8bd252c320",
                        "authState": "ANONYMOUS",
                    },
                    "privacyTrackingState": "CAN_TRACK",
                },
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "e4395701b94b0d775953952e1c7fe66122b183a24cd4cd221a378343108b2512",
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
