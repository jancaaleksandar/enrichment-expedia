# import requests

# from ..logging import log # type: ignore
# from typing import Optional


# def get_proxy_ip(proxies: dict[str, str]) -> Optional[None]:
#     """
#     Get the current proxy IP address.
#     """
#     try:
#         response = requests.get("https://httpbin.org/ip", proxies=proxies)
#         response = response.json() # type: ignore
#     except Exception as e:
#         log(
#             log_path="GET_PROXY_IP",
#             log_message=f"Error getting proxy IP: {e}",
#             log_level="ERROR",
#         )
#         raise e
#     finally:
#         return None


# if __name__ == "__main__":
#     from ..utils.http.http_proxy import get_proxy # type: ignore

#     proxies = get_proxy() # type: ignore
#     get_proxy_ip(proxies) # type: ignore
