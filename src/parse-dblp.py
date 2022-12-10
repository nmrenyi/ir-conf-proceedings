"""
script of parsing paper list from dblp
"""

import argparse
import itertools
import os
from time import sleep
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


def parse_args():
    """
    parse arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', nargs='+',
                        help='<Required> conference names (example: sigir cikm www)', required=True)
    parser.add_argument('-y', '--year', nargs='+',
                        help='<Required> years for the conferences (example: 2022 2021)', required=True)
    parser.add_argument('-t', '--type', nargs='+', default=['tsv', 'md'],
                        help='output file types, default: [''tsv'', ''md''], options: [''tsv'', ''md'']')
    parser.add_argument('-o', '--output_dir', type=str,
                        default='../data/', help='output directory, default: ../data/')
    return parser.parse_args()


def get_page(conf, year):
    """
    get the HTML page from the source, which can be either a url or a local file
    """
    url = f'https://dblp.org/db/conf/{conf}/{conf}{year}.html'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()
    return html_page


def parse_page(page):
    """
    parse HTML page to get the paper list
    """
    soup = BeautifulSoup(page, 'html.parser')
    headers = soup.find_all('h2')
    # the first element is `Refine list`, which is not a session title
    headers.pop(0)
    headers = [header.text.replace('\n', ' ') for header in headers]

    meta_data = soup.find_all('ul', class_='publ-list')
    # the first element is the proceeding information, not paper information
    meta_data.pop(0)
    meta_list = []
    for meta in meta_data:
        session_list = []
        paper_info = meta.find_all('li', class_='entry inproceedings')
        for paper_meta in paper_info:
            title = paper_meta.find('cite').find('span', class_='title').text
            authors = [author.text for author in paper_meta.find('cite').find_all(
                'span', itemprop='author')]
            url = paper_meta.find('nav', class_='publ').find(
                'li').find('a').get('href')
            session_list.append({
                'title': title,
                'authors': ', '.join(authors),
                'url': url
            })
        meta_list.append(session_list)
    assert (len(meta_list) == len(headers))
    paper_list = []
    for i in range(len(meta_list)):
        for paper in meta_list[i]:
            paper_list.append({**paper, **{'session': headers[i]}})
    return paper_list


def save_file(df, output_base_dir, file_type, conf, year):
    """
    save the DataFrame containing information of papers to a file
    """
    if 'tsv' in file_type:
        output_dir = os.path.join(output_base_dir, 'tsv')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(
            output_dir, f'{conf}{year}.tsv')
        df.to_csv(output_path, sep='\t', index=False)

    if 'md' in file_type:
        output_dir = os.path.join(output_base_dir, 'md')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(
            output_dir, f'{conf}{year}.md')
        with open(output_path, 'w') as f:
            # remove redundant whitespace to shrink the file size
            f.write(df.to_markdown(index=False).replace('   ', ''))


def get_dataframe(paper_list):
    """
    convert the paper list to a DataFrame
    """
    return pd.DataFrame(paper_list)


def main():
    args = parse_args()
    print(
        f'confs: {args.conf}, years: {args.year}, output_dir: {args.output_dir}, file_type: {args.type}')
    proceedings = [proceeding for proceeding in itertools.product(
        args.conf, args.year)]
    print(f'{len(proceedings)} proceedings to be processed:')
    print('\n'.join([f'{p[0]}{p[1]}' for p in proceedings]))
    tasks = tqdm(proceedings)
    for conf, year in tasks:
        tasks.set_description(f'Processing {conf} {year}')
        tasks.refresh()  # to show immediately the update
        page = get_page(conf, year)
        paper_list = parse_page(page)
        df = get_dataframe(paper_list)
        save_file(df, args.output_dir, args.type, conf, year)


if __name__ == '__main__':
    main()
