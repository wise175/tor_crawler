from datetime import datetime

from modules.dbConnection import CRUD
# from modules.dbConnection import save_pending_link, next_pending_link, \
#     exist_pending_link, check_link, save_crawled_link, is_offline
from modules.onionLink import OnionLink


class Queue:

    @staticmethod
    def add_link_pending(links, seed=None):
        for link in links:
            if not CRUD.exist_pending_link(link):
                CRUD.save_pending_link(
                    [link, 'false', str(datetime.now()), seed])

    @staticmethod
    def next():
        ID = 0
        URI = 1
        link_data = CRUD.next_pending_link()
        if link_data[ID] == -1:
            return None
        else:
            return {
                'link_pending': link_data[ID],
                'uri': link_data[URI],
            }

    @staticmethod
    def add_crawled_link(onion_link_data, link_pending):
        CRUD.save_crawled_link(onion_link_data)
        CRUD.check_link(link_pending)

    @staticmethod
    def is_parent_offline(uri):
        PARENT_ID = 0
        ERROR_CODE = 1
        parent_domain = OnionLink.netloc(uri)
        result = CRUD.is_offline(parent_domain)
        if result:
            return {
                'id': result[PARENT_ID],
                'code': result[ERROR_CODE]
            }
        return {}
