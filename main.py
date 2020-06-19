import argparse
from multiprocessing import Pool

from modules.onionLink import OnionLink
from modules.queue import Queue
from modules.torConnection import tor_connect


def get_args():
    parser = argparse.ArgumentParser(prog="tor crawler",
                                     usage="Crawling darknet Tor en busca de delitos informaticos.")
    parser.add_argument("-i", "--host",
                        help="Sets host where Tor service is running.")
    parser.add_argument("-p", "--port",
                        help="Sets port where Tor service is running.")
    parser.add_argument("-s", "--seed",
                        help="Text file with onion links seed.")
    return parser.parse_args()


def main():
    args = get_args()
    tor_connect(args.host, args.port)

    if args.seed:
        onion_links_seed = open(args.seed, "r")
        content = onion_links_seed.read().splitlines()
        Queue.add_link_pending(content)

    with Pool(processes=4) as pool:
        pool.apply(crawling, args=())


def crawling():
    next_link = Queue.next()
    while next_link:
        uri = next_link['uri']
        link_pending = next_link['link_pending']
        print("Crawling..."+uri)
        parent_domain_offline = Queue.is_parent_offline(uri)
        if parent_domain_offline:
            on_link = OnionLink(link=uri, link_pending=link_pending,
                                parent_domain_offline=parent_domain_offline)
        else:
            on_link = OnionLink(link=uri, link_pending=link_pending)
        Queue.add_link_pending(on_link.links, on_link.uri)
        Queue.add_crawled_link(on_link.get_fields(), link_pending)
        next_link = Queue.next()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Crawling stopped!!!")
