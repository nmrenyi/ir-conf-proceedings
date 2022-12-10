"""
script of parsing paper list from dblp
"""

import argparse

import pandas as pd
from bs4 import BeautifulSoup


def parse_args():
    """
    parse arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='tsv',
                        help='output file type (default: tsv, options: tsv, md)')
    parser.add_argument(
        '--src', type=str, default='https://dblp.org/db/conf/sigir/sigir2022.html', help='url or absolute path of the source HTML file')
    parser.add_argument('--output_path', type=str,
                        default='../data/tsv/dblp-sigir-2022.tsv', help='output path')
    return parser.parse_args()


def get_page(src):
    """
    get the HTML page from the source, which can be either a url or a local file
    """
    with open('./dblp/dblp-sigir-2022.html', 'r') as f:
        return f.read()


def parse_page(page):
    """
    parse HTML page to get the paper list
    """
    soup = BeautifulSoup(page, 'html.parser')
    paper_list = []
    headers = soup.find_all('h2')
    # the first element is `Refine list`, which is not a session title
    headers.pop(0)

    for id, header in enumerate(headers):
        print(id, header.text.replace('\n', ' '))

    meta_data = soup.find_all('ul', class_='publ-list')
    # the first element is the proceeding information, not paper information
    meta_data.pop(0)
    for id, meta in enumerate(meta_data):
        print(id)
    pass


def save_file(df, output_path, file_type):
    """
    save the DataFrame containing information of papers to a file
    """
    pass


def get_dataframe(paper_list):
    """
    convert the paper list to a DataFrame
    """
    return pd.DataFrame(paper_list)


def main():
    args = parse_args()
    page = get_page(args.src)
    paper_list = parse_page(page)
    df = get_dataframe(paper_list)
    save_file(df, args.output_path, args.type)


if __name__ == '__main__':
    main()
