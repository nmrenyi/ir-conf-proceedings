"""
script of parsing paper list from dblp
"""

import argparse
from urllib.request import Request, urlopen

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
    # with open('./dblp/dblp-sigir-2022.html', 'r') as f:
    #     return f.read()
    url = 'https://dblp.org/db/conf/sigir/sigir2022.html'
    print('Requesting data... (from {})'.format(url))
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


def save_file(df, output_path, file_type):
    """
    save the DataFrame containing information of papers to a file
    """
    if file_type == 'tsv':
        df.to_csv(output_path, sep='\t', index=False)
    elif file_type == 'md':
        with open(output_path, 'w') as f:
            f.write(df[['title', 'authors', 'session', 'abstract', 'url']].to_markdown(
                index=False).replace('   ', ''))  # remove redundant whitespace to shrink the file size
    else:
        raise ValueError('Unsupported file type: {}'.format(file_type))
    print('output saved to {}'.format(output_path))


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
