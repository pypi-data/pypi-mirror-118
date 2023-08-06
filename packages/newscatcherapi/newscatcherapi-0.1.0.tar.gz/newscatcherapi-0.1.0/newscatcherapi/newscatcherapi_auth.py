from requests.auth import AuthBase


class NewsCatcherApiAuth(AuthBase):
    # Provided by NewsCatcher: https://docs.newscatcherapi.com/api-docs/authentication
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update(get_auth_headers(self.api_key))
        return request


def get_auth_headers(api_key):
    return {"Content-Type": "Application/JSON", "x-api-key": api_key}
