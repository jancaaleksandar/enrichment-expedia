import json
import time
from typing import TypedDict, cast

from ...db.models import LeadHotelRunModel
from ..configuration.competitor_search_configuration import (
    get_competitor_search_configuration,
)
from ..utils.http.http_proxy import get_proxy
from ..utils.http.http_request import Request


class CompetitorSearchExecutorResponse(TypedDict):
    successfully_scraped: bool
    response: dict[str, object] | None


def competitor_search_executor(
    params: LeadHotelRunModel, max_retries: int = 3
) -> CompetitorSearchExecutorResponse:
    """
    Execute competitor search using the shared Request helper.

    - Handles retries and 429 cookie capture (bm_s)
    - Returns response with success status and data
    """
    successfully_scraped = False
    response = None
    persistent_cookies: dict[str, str] = {}

    try:
        for attempt in range(max_retries):
            try:
                request_params = get_competitor_search_configuration(params=params)
                with open("request_params.json", "w") as f:
                    json.dump(request_params, f)
                # Wire proxy required by Request helper
                request_params["request_proxy"] = get_proxy("EUROPE")
                # Persist cookies across attempts
                request_params["request_cookies"] = persistent_cookies or None

                resp = Request(params=request_params).curl_request_api_post()
                resp_obj = resp["response"]

                if resp_obj.status_code == 200:
                    print("200 status code...")
                    response = cast(dict[str, object], resp_obj.json())  # type: ignore
                    successfully_scraped = True
                    break  # Exit loop on success

                if resp_obj.status_code == 429:
                    print("429 status code... retrying in 6 seconds")

                    # Extract cookies for next attempt
                    try:
                        if hasattr(resp_obj, "cookies") and resp_obj.cookies:
                            cookies_dict = {
                                name: value for name, value in resp_obj.cookies.items()
                            }
                            print(f"⚠️  429 cookies found: {len(cookies_dict)} cookies")
                            if "bm_s" in cookies_dict:
                                persistent_cookies["bm_s"] = cookies_dict["bm_s"]
                                print("🎯 Captured bm_s from 429 response")
                    except Exception as cookie_error:  # noqa: BLE001
                        print(
                            f"Error extracting cookies from 429 response: {cookie_error}"
                        )

                    time.sleep(6)
                    continue

                print(f"Unexpected status code: {resp_obj.status_code}")

            except (
                ValueError,
                ConnectionError,
                TimeoutError,
                json.JSONDecodeError,
            ) as e:
                print(f"Exception occurred in attempt {attempt + 1}: {e!s}")

            print(f"Attempt {attempt + 1} failed, continuing to next attempt")

    except (ValueError, ConnectionError, TimeoutError, json.JSONDecodeError) as e:
        print(f"Fatal error in competitor search: {e!s}")
        successfully_scraped = False
        response = None

    finally:
        pass

    return CompetitorSearchExecutorResponse(
        successfully_scraped=successfully_scraped, response=response
    )
