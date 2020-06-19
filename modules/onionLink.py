import socket
import urllib
from http.client import RemoteDisconnected, IncompleteRead, BadStatusLine
from ssl import SSLCertVerificationError
from urllib.parse import urlparse
from urllib.request import urlopen

import validators as validators
from bs4 import BeautifulSoup
from socks import GeneralProxyError, SOCKS5AuthError, SOCKS5Error
from urllib3.util import timeout

STATE = {
    'available': "Online",
    'not_available': "Offline",
}

FILES = [
    '.jpg', '.zip', '.png', '.jpeg', '.mp4', '.webm', '.gif', '.bmp'
]


class OnionLink:

    def __init__(self, link, parent=None, seed=None, link_pending=None,
                 parent_domain_offline=[]):
        if not self.is_valid(link):
            raise ValueError(f'"Invalid link: "{link}')

        self.name = "NOT TITLE"
        self._children = []
        self._links = []
        self._metadata = {}
        self._http_code = None
        self._parent = parent
        self.error = None
        self._node = ""
        self._uri = link
        self._link_pending = link_pending
        self._state = STATE['available']
        self._description = ""
        self.response = None

        if parent_domain_offline:
            self.failure(parent_domain_offline['code'])
            return
        if list(filter(link.endswith, FILES)):
            self.failure('file')
            return
        try:
            if not parent_domain_offline:
                self.response = urlopen(link, timeout=25)
        except urllib.error.URLError as e:
            if e and isinstance(e.reason, str):
                self.failure(e.reason)
                return
            if e and isinstance(e.reason, GeneralProxyError):
                self.failure(e.reason.socket_err)
                return
            if e and isinstance(e.reason, SSLCertVerificationError):
                self.failure(e.reason)
                return
            self.failure(e.reason.msg)
            return
        except urllib.error.HTTPError as e:
            if e and isinstance(e.reason, str):
                self.failure(e.reason)
            self.failure(e.reason.msg)
            return
        except UnicodeEncodeError as e:
            self.failure(str(e))
            return
        except RemoteDisconnected as e:
            self.failure(str(e))
            return
        except GeneralProxyError as e:
            self.failure(e.socket_err)
            return
        except SOCKS5AuthError as e:
            self.failure(e.socket_err)
            return
        except SOCKS5Error as e:
            self.failure(e.socket_err)
            return
        except BadStatusLine as e:
            self.failure(str(e))
            return
        except socket.timeout as e:
            self.failure(str(e))
            return
        except timeout as e:
            self.failure(str(e.socket_err))
            return
        except SSLCertVerificationError as e:
            self.failure(str(e))
            return
        except Exception as e:
            self.failure(str(e))
            return

        try:
            self._node = BeautifulSoup(self.response.read(), 'html.parser')
        except IncompleteRead as e:
            self.failure(str(e))
            return
        except TypeError as e:
            self.failure(str(e))
            return
        except UnboundLocalError as e: # caracteres especiales
            self.failure(str(e))
            return
        except socket.timeout as e:
            self.failure(str(e))
            return
        except timeout as e:
            self.failure(str(e.socket_err))
            return

        if not self._node.title:
            self.name = "NOT TITLE"
        elif self._node.title.string:
            self.name = self._node.title.string
        else:
            self.name = "NOT TITLE"

    def failure(self, reason):
        print("Unable to reach %s" % self._uri)
        self._state = STATE['not_available']
        self.error = str(reason)
        self.name = str(reason)
        return

    @property
    def metadata(self):
        if not self._metadata:
            self._metadata = self.response.info()
        return self._metadata

    @property
    def http_code(self):
        if not self._http_code:
            if self.response:
                self._http_code = self.response.getcode()
            else:
                self._http_code = self.error
        return self._http_code

    @property
    def uri(self):
        return self._uri

    @property
    def description(self):
        if not self._description and self._node != "":
            for tag in self._node.findAll("meta"):
                name = tag.get('name')
                if name and name == 'description':
                    description = tag.get('content')
                    if description is None:
                        description = ""
                    self._description = description
        return self._description

    @property
    def children(self):
        if not self._children and self._node:
            self._children = self._node.find_all('a')
        return self._children

    @property
    def html_string(self):
        if self._node:
            return self._node.prettify()
        return ""

    @property
    def links(self):
        if not self._links:
            links = []
            refs = [x.get('href') for x in self.children]
            for ref in refs:
                if ref and self.is_valid(ref) and ref != self._uri:
                    if not list(filter(self._uri.endswith, FILES)):
                        links.append(ref)
            links.sort()
            print(f'{len(links)} Links found on {self._uri}')

            self._links = links
        return self._links

    @staticmethod
    def netloc(link):
        if OnionLink.is_valid(link):
            parsed_uri = urlparse(link)
            netloc = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            return netloc
        else:
            return None

    @staticmethod
    def is_valid(link):
        if 'onion' in link and validators.url(link):
            return True
        return False

    def get_fields(self):
        return [self.name, self.description, self.html_string, self._state,
                self.netloc(self._uri), self.http_code, self._link_pending]
