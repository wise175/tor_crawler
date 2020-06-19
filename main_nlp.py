import argparse
from multiprocessing import Pool

from modules.crimeIdentification import identification
from modules.dbConnection import save_analized_link
from modules.nlp import analysis


def get_args():
    parser = argparse.ArgumentParser(prog="Crime Analysis",
                                     usage="Analisis de contenidos de servicios ocultos en busca de delitos informaticos.")
    parser.add_argument("-i", "--host",
                        help="Sets host where Tor service is running.")
    parser.add_argument("-p", "--port",
                        help="Sets port where Tor service is running.")
    return parser.parse_args()


def main_nlp():
    args = get_args()

    with Pool(processes=4) as pool:
        pool.apply(nlp_analysis, args=())


def nlp_analysis():
    nlp_analysis = analysis()
    while nlp_analysis:
        result = identification(nlp_analysis)
        save_analized_link(result)
        nlp_analysis = analysis()


if __name__ == '__main__':
    try:
        main_nlp()
    except KeyboardInterrupt:
        print("Crime Analysis stopped!!!")
