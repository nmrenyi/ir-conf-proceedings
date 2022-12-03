"""
script of parsing the paper list of SIGIR 2022 from https://sigir.org/sigir2022/program/proceedings/
"""
import argparse
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import trange

from utils import parse_args, parse_html, save_file


def append_paper(paper_list, paper, session_name):
    paper['session'] = session_name
    paper_list.append(paper)
    return paper_list


def main():
    all_papers = parse_html(
        url='https://sigir.org/sigir2022/program/proceedings/', target_id='DLcontent')

    args = parse_args()

    info_list = []
    info = {}
    session_name = ''

    for i in trange(len(all_papers)):
        line = all_papers.contents[i]
        if line.name == 'h2':
            if info:
                info_list = append_paper(info_list, info, session_name)
                info = {}
                session_name = ''
            session_name = line.text
        elif line.name == 'h3':
            if info:
                info_list = append_paper(info_list, info, session_name)
                info = {}
            info['title'] = line.text
            info['url'] = line.find('a').get('href')
        elif line.name == 'ul':
            info['authors'] = ', '.join([r.text for r in line.find_all('li')])
        elif line.name == 'div':
            info['abstract'] = '\n\n'.join(
                [r.text for r in line.find_all('p')])

    if info:
        info_list = append_paper(info_list, info, session_name)
        info = {}

    df = pd.DataFrame(info_list)[
        ['title', 'authors', 'session', 'url', 'abstract']]
    print(df.info())

    file_type = args.type
    output_path = '../data/{0}/sigir2022.{0}'.format(file_type)

    save_file(df, output_path, file_type)


if __name__ == '__main__':
    main()
