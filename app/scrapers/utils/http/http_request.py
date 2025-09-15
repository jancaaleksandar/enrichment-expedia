from __future__ import annotations

import asyncio
import random
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from curl_cffi import requests
from curl_cffi.const import CurlOpt
from curl_cffi.requests import ExtraFingerprints, Response

from app.scrapers.types.http import RequestParameters, SyncResponse

PATCH_POOL = [
    "7103.32",
    "7103.48",
    "7103.49",
    "7103.93",
    "7103.94",
    "7103.113",
    "7103.114",
]

patch = random.choice(PATCH_POOL)
# ──────────────────────────────────────────────────────────────────────────────
#  AUTHENTIC BROWSER PROFILES (curl‑cffi v0.12)
# ──────────────────────────────────────────────────────────────────────────────
PROFILES: dict[str, dict[str, Any]] = {
    # ---------- Chrome 136 ----------------------------------------------------
    "chrome136": {
        "sig_algs": [
            "ecdsa_secp256r1_sha256",
            "ecdsa_secp384r1_sha384",
            "rsa_pss_rsae_sha256",
            "rsa_pss_rsae_sha384",
            "rsa_pss_rsae_sha512",
            "rsa_pkcs1_sha256",
            "rsa_pkcs1_sha384",
            "rsa_pkcs1_sha1",
        ],
        "headers": {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7"
            ),
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua": (
                '"Chromium";v="136", "Google Chrome";v="136", "Not A;Brand";v="24"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        },
        "h2_range": {
            "HEADER_TABLE_SIZE": [16384, 65536],
            "INITIAL_WINDOW_SIZE": [6291456],
            "MAX_CONCURRENT_STREAMS": [100, 256, 1000],
            "MAX_HEADER_LIST_SIZE": [262144, 524288],
        },
    },
}

PROFILE_NAMES: List[str] = list(PROFILES.keys())


class Request:
    def __init__(self, params: RequestParameters) -> None:
        self.params = params
        self.impersonation = random.choice(PROFILE_NAMES)
        self.profile = PROFILES[self.impersonation]
        self.randomized_headers: Dict[str, str] = {}
        self.curl_opts: Dict[int, Any] = {}

    # ---------- timing utilities ----------
    @staticmethod
    def _micro_pause() -> None:
        time.sleep(
            random.choices(
                [random.uniform(0.05, 0.2), random.uniform(0.5, 2.0)],
                weights=[0.9, 0.1],
            )[0]
        )

    @staticmethod
    def _backoff_sync(attempt: int) -> None:
        back = max(1, min(30, 2**attempt))
        time.sleep(back * random.uniform(0.5, 1.5))

    @staticmethod
    async def _backoff_async(attempt: int) -> None:
        back = max(1, min(30, 2**attempt))
        await asyncio.sleep(back * random.uniform(0.5, 1.5))

    @staticmethod
    def _short_jitter() -> None:
        time.sleep(random.uniform(0.1, 0.5))

    @staticmethod
    async def _short_jitter_async() -> None:
        await asyncio.sleep(random.uniform(0.1, 0.5))

    # ---------- fingerprint + headers -------
    def _build_fp_and_headers(self) -> ExtraFingerprints:
        reuse = random.random() < 0.75
        alpn_on = 1
        if not reuse and random.random() < 0.1:
            alpn_on = 0  # HTTP/1.1 trial

        self.curl_opts = {
            CurlOpt.FRESH_CONNECT: 1,
            CurlOpt.FORBID_REUSE: 1,
            CurlOpt.SSL_SESSIONID_CACHE: int(reuse),
            CurlOpt.SSL_ENABLE_TICKET: int(reuse),
            CurlOpt.SSL_ENABLE_ALPN: alpn_on,
            CurlOpt.CONNECTTIMEOUT_MS: 8000,
            CurlOpt.LOW_SPEED_TIME: 15,
        }

        sigs = self.profile["sig_algs"].copy()
        sigs = sigs[:4] + random.sample(sigs[4:], len(sigs) - 4)

        # Only add tls_cert_compression when we actually want Brotli
        fp_kwargs: Dict[str, Any] = dict(
            tls_grease=True,
            tls_permute_extensions=False,
            tls_signature_algorithms=sigs,
        )
        # Chrome / Edge sometimes advertise Brotli; Safari never does
        if not self.impersonation.startswith("safari") and random.random() < 0.5:
            fp_kwargs["tls_cert_compression"] = "brotli"

        fp = ExtraFingerprints(**fp_kwargs)

        rng = self.profile["h2_range"]
        http2_settings = (
            f"HEADER_TABLE_SIZE={random.choice(rng['HEADER_TABLE_SIZE'])},"
            f"INITIAL_WINDOW_SIZE={random.choice(rng['INITIAL_WINDOW_SIZE'])},"
            f"MAX_CONCURRENT_STREAMS={random.choice(rng['MAX_CONCURRENT_STREAMS'])},"
            f"MAX_HEADER_LIST_SIZE={random.choice(rng['MAX_HEADER_LIST_SIZE'])}"
        )
        setattr(fp, "http2_settings", http2_settings)

        hdrs: Dict[str, str] = self.profile["headers"].copy()
        if alpn_on == 0:
            hdrs["host"] = urlparse(self.params["url"]).netloc
        if self.params["request_headers"]:
            hdrs.update(
                {k.lower(): v for k, v in self.params["request_headers"].items()}
            )

        stable = [
            "host",
            "user-agent",
            "accept",
            "accept-encoding",
            "accept-language",
            "sec-ch-ua",
            "sec-ch-ua-mobile",
            "sec-ch-ua-platform",
        ]
        tail = [h for h in hdrs if h not in stable]
        random.shuffle(tail)
        order = [h for h in stable if h in hdrs] + tail

        self.randomized_headers = {k: hdrs[k] for k in order}
        setattr(fp, "header_order", order)
        self._micro_pause()
        return fp

    # ---------- helper for normal GET/POST ---
    def _do_sync(
        self,
        method: str,
        *,
        cookies: Optional[Dict[str, str]] = None,
        data: Any = None,
        params: Any = None,
    ) -> SyncResponse:
        try:
            proxy_url = self.params["request_proxy"]
            if not proxy_url:
                raise Exception("No proxy URL provided")
            proxy = {"https": proxy_url, "http": proxy_url}
            fp = self._build_fp_and_headers()
            response: Response = getattr(requests, method)(
                self.params["url"],
                headers=self.randomized_headers,
                data=data,
                params=params,
                impersonate=self.impersonation,
                proxies=proxy,
                extra_fp=fp,
                curl_options=self.curl_opts,
                verify=True,
                allow_redirects=True,
                timeout=random.uniform(20, 35),
                cookies=cookies or {},
            )
            return SyncResponse(
                response=response,
                fingerprint=fp,
                request_headers=self.randomized_headers,
            )
        except Exception as e:
            raise e

    # ---------- dedicated cookie fetch -------
    def curl_request_cookie(self) -> Optional[str]:
        try:
            proxy_url = self.params["request_proxy"]
            if not proxy_url:
                raise Exception("No proxy URL provided")
            proxy = {"https": proxy_url, "http": proxy_url}
            fp = self._build_fp_and_headers()
            resp: Response = requests.get(
                self.params["url"],
                headers=self.randomized_headers,
                impersonate=self.impersonation,  # type: ignore[arg-type]
                proxies=proxy,  # type: ignore[arg-type]
                extra_fp=fp,
                curl_options=self.curl_opts,
                verify=True,
                allow_redirects=True,
                timeout=random.uniform(20, 35),
                cookies={},
            )
            if resp.status_code == 200 and resp.cookies:
                return "; ".join(
                    f"{name}={value}" for name, value in resp.cookies.items()
                )
        except Exception as e:
            raise e

    # ---------- public wrappers --------------
    def curl_request_api_post(self) -> SyncResponse:
        return self._do_sync(
            method="post",
            cookies=self.params["request_cookies"],
            data=self.params["request_body"],
        )

    def curl_request_api_get(self) -> SyncResponse:
        return self._do_sync(
            "get",
            cookies=self.params["request_cookies"],
            params=self.params["request_body"],
        )

    def curl_request_html_get(self) -> SyncResponse:
        return self._do_sync(
            "get",
            cookies=self.params["request_cookies"],
            params=self.params["request_body"],
        )
