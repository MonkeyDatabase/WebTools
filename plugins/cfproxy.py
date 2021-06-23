import requests
from urllib.parse import urlparse
from lib.classtype import TypePlugin


class Plugin(TypePlugin):
    """proxy using cloudflare workers
    """
    priority = 3

    TOKEN_HEADER = 'Px-Token'
    TOKEN_VALUE = 'mysecuretoken'
    HOST_HEADER = 'Px-Host'
    IP_HEADER = 'Px-IP'

    def __init__(self, proxy_host: str, user_agent: str, fake_ip: str, proxy=None):
        self.session = requests.Session()
        self.session.proxies.update({
            'https': proxy,
            'http': proxy
        })
        self.session.headers.update({
            'User-Agent': user_agent,
            self.TOKEN_HEADER: self.TOKEN_VALUE
        })
        self.proxy_host = proxy_host
        self.fake_ip = fake_ip

    def request(self, method, url, **kwargs):
        if 'headers' in kwargs:
            for k, v in kwargs.get('headers'):
                self.session.headers.update({k: v})
            kwargs.pop('headers')
        parsed_uri = urlparse(url)
        self.session.headers.update({self.HOST_HEADER: parsed_uri.hostname})
        self.session.headers.update({self.IP_HEADER: self.fake_ip})
        proxyfied_uri = '{0}://{1}{2}'.format(parsed_uri.scheme, self.proxy_host, parsed_uri.path)
        return self.session.request(method, proxyfied_uri, **kwargs)

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def get_source(self):
        pass
