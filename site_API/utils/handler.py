from typing import Dict

from requests import codes, request


def make_response(method: str, url: str,
                  headers: Dict, params: Dict, timeout=10, success=codes.ok):
    response = request(
        method,
        url,
        headers=headers,
        params=params,
        timeout=timeout
    )

    status_code = response.status_code

    if status_code == success:
        return response

    return status_code


def get_city_hotels(method: str, url: str, headers: Dict,
                    params: Dict, func=make_response):
    url = f"{url}/v2/get-meta-data"
    response = func(method, url, headers=headers, params=params)
    return response


class SiteApiInterface:
    @staticmethod
    def get_city_hotels():
        return get_city_hotels


if __name__ == "__main__":
    make_response()
    get_city_hotels()
    SiteApiInterface()
