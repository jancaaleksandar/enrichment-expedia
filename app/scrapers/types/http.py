from typing import Dict, Literal, Optional, TypedDict

from curl_cffi.requests import ExtraFingerprints, Response


class SyncResponse(TypedDict):
    response: Response
    fingerprint: ExtraFingerprints
    request_headers: Dict[str, str]


class RequestParameters(TypedDict):
    url: str
    request_proxy: str
    request_headers: Optional[Dict[str, str]]
    request_cookies: Optional[Dict[str, str]]
    request_body: Optional[str]
    request_type: Literal["GET", "POST"]
