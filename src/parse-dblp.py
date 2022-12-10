"""
script of parsing paper list from dblp
"""


def parse_args():
    pass


def get_page(src):
    pass


def parse_page(page):
    pass


def save_file(df, output_path, file_type):
    pass


def main():
    args = parse_args()
    page = get_page(args.src)
    paper_list = parse_page(page)
    df = pd.DataFrame(paper_list)[
        ['title', 'authors', 'session', 'abstract', 'url']]
    save_file(df, args.output_path, args.type)


if __name__ == '__main__':
    main()
