import argparse
from multiprocessing import Pool

from modules.crimeIdentification import CrimeCategorization
from modules import dbConnection
from modules.dbConnection import CRUD
from modules.nlp import NLP


def get_args():
    parser = argparse.ArgumentParser(prog="Crime Analysis",
                                     usage="Analisis de contenidos de "
                                           "servicios ocultos en busca de "
                                           "delitos informaticos.")
    parser.add_argument("-i", "--host",
                        help="Sets host where Tor service is running.")
    parser.add_argument("-p", "--port",
                        help="Sets port where Tor service is running.")
    parser.add_argument("-c", "--config-file",
                        help="Sets config file where where some properties "
                             "are,such as the connection to the Database.")
    return parser.parse_args()


def main_nlp():
    args = get_args()
    params_conn = dbConnection.get_connection(args.config_file)
    dbConnection.connection = params_conn.get('conn')
    dbConnection.cursor = params_conn.get('cursor')

    with Pool(processes=4) as pool:
        pool.apply(nlp_analysis, args=())


def nlp_analysis():
    nlp = NLP()
    crime_cat = CrimeCategorization()
    nlp_analysis = nlp.analysis(CRUD.next_pending_content())
    while nlp_analysis:
        result = crime_cat.identification(nlp_analysis)
        CRUD.save_analized_link(result)
        nlp_analysis = nlp.analysis(CRUD.next_pending_content())


if __name__ == '__main__':
    try:
        main_nlp()
    except KeyboardInterrupt:
        print("Crime Analysis stopped!!!")
