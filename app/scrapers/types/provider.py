from typing import Optional, TypedDict


class Provider(TypedDict):
    provider_name: Optional[str]
    provider_offer_url: Optional[str]
    provider_offer_is_brand_offer: Optional[bool]
    provider_offer_price_amount: Optional[float]
    provider_offer_price_currency: Optional[str]
    provider_offer_is_sold_out: bool
    provider_icon_url: Optional[str]
