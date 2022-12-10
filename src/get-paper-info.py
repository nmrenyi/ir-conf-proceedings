"""
script for getting paper information (e.g. abstract) from https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper_search
"""
import json
from datetime import datetime
from time import sleep

import pandas as pd
import requests
from tqdm import tqdm


def main():
    df = pd.read_csv('../data/tsv/sigir2022.tsv', sep='\t')
    print(df.info())
    urls = df['url'].tolist()

    abstract_list = []
    for i, url in enumerate(tqdm(urls)):
        doi = url.replace('https://doi.org/', '')
        paper_url = f'https://api.semanticscholar.org/graph/v1/paper/{doi}?fields=abstract'
        while True:
            r = requests.get(paper_url)
            if r.status_code == 200:
                abstract_list.append(json.loads(r.text)['abstract'])
                break
            else:
                print(
                    f'Error: {r.status_code, r.text}, sleep for 5 minutes and retry, current time: {datetime.now()}')
                sleep(5 * 60)

    df['abstract'] = abstract_list
    df.to_csv('./sigir2022.tsv', sep='\t', index=False)


if __name__ == '__main__':
    main()
