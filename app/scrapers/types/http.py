from typing import Literal, TypedDict

from curl_cffi.requests import ExtraFingerprints, Response


class SyncResponse(TypedDict):
    response: Response
    fingerprint: ExtraFingerprints
    request_headers: dict[str, str]


class RequestParameters(TypedDict):
    url: str
    request_proxy: str
    request_headers: dict[str, str] | None
    request_cookies: dict[str, str] | None
    request_body: str | None
    request_type: Literal["GET", "POST"]
