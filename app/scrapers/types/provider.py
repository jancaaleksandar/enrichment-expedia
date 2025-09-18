from typing import TypedDict


class Provider(TypedDict):
    provider_name: str | None
    provider_offer_url: str | None
    provider_offer_is_brand_offer: bool | None
    provider_offer_price_amount: float | None
    provider_offer_price_currency: str | None
    provider_offer_is_sold_out: bool
    provider_icon_url: str | None
