from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from .error import NotFoundError, NotURLError
from urllib.parse import urljoin, urlparse
from itertools import product
import re

class Parse(dict):
    def __init__(self, url, requests=False, **kwargs):
        """
        Parse robots.txt and returns a Parse instance.

        >>> p = Parse("https://www.google.com/")
        >>> {'*': ~~}
        >>> Returns the Parse type of description for each User-Agent.
        """
        if not url.endswith("robots.txt"):
            url = urljoin(url, "/robots.txt")
        self._get_home(url)
        result = request(url, use_requests=requests, option=kwargs)
        data = parse(result.splitlines())
        super().__init__(**data)

    def _get_home(self, url):
        parsed = urlparse(url)
        if parsed.scheme:
            self.home = f"{parsed.scheme}://{parsed.netloc}"
        else:
            raise NotURLError(f"'{url}' is not url")

    def _delete_query(self, url):
        question = url.find("?")
        if 0 < question:
            return url[:question]
        else:
            return url

    def Allow(self, useragent="*"):
        """
        Get allow list from robots.txt.
        If there was nothing, return None.
        """
        data = self.get(useragent)
        if data:
            return data.get("Allow")

    def Disallow(self, useragent="*"):
        """
        Get disallow list from robots.txt.
        If there was nothing, return None
        """
        data = self.get(useragent)
        if data:
            return data.get("Disallow")

    def delay(self, useragent="*"):
        data = self.get(useragent)
        if data:
            return data.get("Crawl-delay")

    def can_crawl(self, url, useragent="*"):
        """
        Returns True if crawl is allowed, False otherwise.
        """
        if not isinstance(url, str):
            raise ValueError("'url' argument must give a string type")
        if not url.startswith(self.home):
            return True
        disallow = self.Disallow(useragent)
        allow = self.Allow(useragent)
        link = url[len(self.home):]
        if allow:
            for a in map(self._delete_query, allow):
                if a != "/" and (link.startswith(a) or re.match(rf".*{a}.*", link)):
                    return True
        if disallow:
            for d in map(self._delete_query, disallow):
                if d != "/" and (link.startswith(d) or re.match(rf".*{d}.*", link)):
                    return False
        return True
                

def request(url, *, use_requests=False, option={}):
    """
    Send a request to robots.txt.
    If use_requests argument is True, use requests module at the time of request
    """
    try:
        if use_requests:
            import requests
            r = requests.get(url, **option)
            if 400 <= r.status_code:
                raise NotFoundError(f"Status code {r.status_code} was returned")
            else:
                result = r.text
        else:
            with urlopen(url, **option) as r:
                result = r.read().decode()
        return result
    except (URLError, HTTPError) as e:
        raise NotFoundError(e)

def parse(info):
    """
    Parse robots.txt
    """
    datas = {}
    for i in info:
        if not i or i.startswith("#"):
            continue
        if i.startswith("User-agent: "):
            useragent = i[12:]
            datas[useragent] = {}
        elif i.startswith("Sitemap: "):
            url = i[9:]
            if "Sitemap" not in datas:
                datas["Sitemap"] = []
            datas["Sitemap"].append(url)
        else:
            split = i.split(": ")
            name = split[0]
            data = split[1]
            if name not in datas[useragent]:
                datas[useragent][name] = []
            datas[useragent][name].append(data)
    return datas