"""
script of parsing paper list from dblp
"""

import pandas as pd


def parse_args():
    pass


def get_page(src):
    with open('./dblp/dblp-sigir-2022.html', 'r') as f:
        return f.read()


def parse_page(page):
    pass


def save_file(df, output_path, file_type):
    pass


def get_dataframe(paper_list):
    return pd.DataFrame(paper_list)[
        ['title', 'authors', 'session', 'abstract', 'url']]


def main():
    args = parse_args()
    page = get_page(args.src)
    paper_list = parse_page(page)
    df = get_dataframe(paper_list)
    save_file(df, args.output_path, args.type)


if __name__ == '__main__':
    main()
