import json
import time
from typing import Dict, TypedDict

from ...db.models import LeadHotelRunModel
from ..configuration.competitor_search_configuration import (
    get_competitor_search_configuration,
)
from ..utils.http.http_proxy import get_proxy
from ..utils.http.http_request import Request


class CompetitorSearchExecutorResponse(TypedDict):
    successfully_scraped: bool
    response: dict | None


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
    persistent_cookies: Dict[str, str] = {}

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
                response = resp["response"]

                if response.status_code == 200:
                    print("200 status code...")
                    response = response.json()
                    successfully_scraped = True
                    break  # Exit loop on success

                if response.status_code == 429:
                    print("429 status code... retrying in 6 seconds")

                    # Extract cookies for next attempt
                    try:
                        if hasattr(response, "cookies") and response.cookies:
                            cookies_dict = {
                                name: value for name, value in response.cookies.items()
                            }
                            print(f"⚠️  429 cookies found: {len(cookies_dict)} cookies")
                            if "bm_s" in cookies_dict:
                                persistent_cookies["bm_s"] = cookies_dict["bm_s"]
                                print("🎯 Captured bm_s from 429 response")
                    except Exception as cookie_error:
                        print(
                            f"Error extracting cookies from 429 response: {cookie_error}"
                        )

                    time.sleep(6)
                    continue

                print(f"Unexpected status code: {response.status_code}")

            except Exception as e:
                print(f"Exception occurred in attempt {attempt + 1}: {str(e)}")

            print(f"Attempt {attempt + 1} failed, continuing to next attempt")

    except Exception as e:
        print(f"Fatal error in competitor search: {str(e)}")
        successfully_scraped = False
        response = None

    finally:
        return CompetitorSearchExecutorResponse(
            successfully_scraped=successfully_scraped, response=response
        )
