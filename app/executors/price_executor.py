from ..db.models import LeadHotelRunModel
from ..configuration.price_configuration import get_price_configuration
from ..utils.http.http_request import Request

def price_executor(params : LeadHotelRunModel, max_retries : int = 15) -> None:
    
    price_configuration = get_price_configuration(params)
    
    for i in range(max_retries):
        request = Request(params=price_configuration)
        response = request.curl_request_api_post()
        if response['response'].status_code == 200:
            break
        elif response['response'].status_code == 429:
            # * cookie logic 429
            if hasattr(response['response'], 'cookies'):
                cookie_jar = response['response'].cookies
                cookies_dict = {name: value for name, value in cookie_jar.items()}
                
                if 'bm_s' in cookies_dict:
                    persisten_cookies['bm_s'] = cookies_dict['bm_s']
                    print(f"Cookie bm_s found and added to persistent cookies")
            else:
                pass
            