from settings import SiteSettings
from site_API.utils.handler import SiteApiInterface

site = SiteSettings()

headers = {
    "X-RapidAPI-Key": site.api_key.get_secret_value(),
    "X-RapidAPI-Host": site.host_api
}

url = "https://" + site.host_api
params = {"fragment": "true", "json": "true"}

site_api = SiteApiInterface()

if __name__ == "__main__":
    site_api()
