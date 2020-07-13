import argparse
from configparser import ConfigParser
from multiprocessing import Pool

import psycopg2

from modules import dbConnection
from modules.onionLink import OnionLink
from modules.torConnection import TorConnection


class Main:

    @staticmethod
    def main():
        def get_args():
            parser = argparse.ArgumentParser(prog="tor crawler",
                                             usage="Crawling darknet Tor en "
                                                   "busca de delitos "
                                                   "informaticos.")
            parser.add_argument("-c", "--config-file",
                                help="Sets config file where where some "
                                     "properties are,such as the connection to"
                                     " the Database.")
            parser.add_argument("-i", "--host",
                                help="Sets host where Tor service is running.")
            parser.add_argument("-p", "--port",
                                help="Sets port where Tor service is running.")
            parser.add_argument("-s", "--seed",
                                help="Text file with onion links seed.")
            return parser.parse_args()

        def crawling():
            next_link = Queue.next()
            while next_link:
                uri = next_link['uri']
                link_pending = next_link['link_pending']
                print("Crawling..." + uri)
                parent_domain_offline = Queue.is_parent_offline(uri)
                if parent_domain_offline:
                    on_link = OnionLink(link=uri, link_pending=link_pending,
                                        parent_domain_offline=
                                        parent_domain_offline)
                else:
                    on_link = OnionLink(link=uri, link_pending=link_pending)
                Queue.add_link_pending(on_link.links, on_link.uri)
                Queue.add_crawled_link(on_link.get_fields(), link_pending)
                next_link = Queue.next()

        args = get_args()
        TorConnection.tor_connect(args.host, args.port)

        params_conn = dbConnection.get_connection(args.config_file)
        dbConnection.connection = params_conn.get('conn')
        dbConnection.cursor = params_conn.get('cursor')

        if args.seed:
            from modules.queue import Queue
            onion_links_seed = open(args.seed, "r")
            content = onion_links_seed.read().splitlines()
            Queue.add_link_pending(content)

        with Pool(processes=4) as pool:
            pool.apply(crawling(), args=())


if __name__ == '__main__':
    try:
        Main().main()
    except KeyboardInterrupt:
        print("Crawling stopped!!!")
