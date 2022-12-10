"""
script of parsing paper list from dblp
"""

import argparse

import pandas as pd


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
