import json
import time
from typing import TypedDict, cast

from ...db.models import LeadHotelRunModel
from ..configuration.price_configuration import get_price_configuration
from ..utils.http.http_proxy import get_proxy
from ..utils.http.http_request import Request


class PriceExecutorResponse(TypedDict):
    successfully_scraped: bool
    response: dict[str, object] | None


def price_executor(
    params: LeadHotelRunModel, max_retries: int = 3
) -> PriceExecutorResponse:
    """
    Execute price search using the shared Request helper.

    - Handles retries and 429 cookie capture (bm_s)
    - Returns response with success status and data
    """
    successfully_scraped = False
    response = None
    persistent_cookies: dict[str, str] = {}

    try:
        for attempt in range(max_retries):
            try:
                price_configuration = get_price_configuration(params=params)
                # Save request params for debugging
                with open("request_params.json", "w") as f:
                    json.dump(price_configuration, f, indent=4)

                # Wire proxy required by Request helper
                price_configuration["request_proxy"] = get_proxy("EUROPE")
                # Persist cookies across attempts
                price_configuration["request_cookies"] = persistent_cookies or None

                resp = Request(params=price_configuration).curl_request_api_post()
                resp_obj = resp["response"]

                if resp_obj.status_code == 200:
                    print("200 status code...")
                    try:
                        response = resp_obj.json()  # type: ignore
                        with open("price_response.json", "w") as f:
                            json.dump(response, f, indent=4)
                        successfully_scraped = True
                        break  # Exit loop on success
                    except ValueError as e:
                        print(f"Failed to parse JSON response: {e!s}")
                        # Save raw response for debugging
                        with open("raw_price_response.txt", "w") as f:
                            f.write(resp_obj.text)

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
                    except ValueError as cookie_error:
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
        print(f"Fatal error in price search: {e!s}")
        successfully_scraped = False
        response = None

    return PriceExecutorResponse(
        successfully_scraped=successfully_scraped,
        response=cast(dict[str, object] | None, response),
    )
