"""
script of parsing the paper list of SIGIR 2022 from https://sigir.org/sigir2022/program/proceedings/
"""
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import trange


def append_paper(paper_list, paper, session_name):
    paper['session'] = session_name
    paper_list.append(paper)
    return paper_list


def main():
    url = 'https://sigir.org/sigir2022/program/proceedings/'
    print('Requesting data... (from {})'.format(url))

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print('Reading data...')
    html_page = urlopen(req).read()

    print('Parsing data...')
    soup = BeautifulSoup(html_page, 'html.parser')
    all_papers = soup.find(id='DLcontent')

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

    output_file = '../data/sigir2022'
    file_type = 'tsv'
    output_path = '{}.{}'.format(output_file, file_type)

    if file_type == 'tsv':
        df.to_csv(output_path, sep='\t', index=False)
    elif file_type == 'md':
        with open(output_path, 'w') as f:
            f.write(df.to_markdown(index=False))
    else:
        raise ValueError('Unsupported file type: {}'.format(file_type))
    print('output saved to {}'.format(output_path))


if __name__ == '__main__':
    main()
