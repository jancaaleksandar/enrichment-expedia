from typing import Dict, TypedDict, Optional, Literal
from curl_cffi.requests import Response, ExtraFingerprints

class SyncResponse(TypedDict):
    response : Response
    fingerprint : ExtraFingerprints
    request_headers : Dict[str, str]

class RequestParameters(TypedDict):
    url : str
    request_proxy : str
    request_headers : Optional[Dict[str, str]]
    request_cookies : Optional[Dict[str, str]]
    request_body : Optional[str]
    request_type : Literal["GET", "POST"]