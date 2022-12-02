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
    url = 'https://sigir.org/sigir2022/program/proceedings/...'
    print('Requesting data from {}'.format(url))

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
            info['authors'] = line.find('li').text
        elif line.name == 'div':
            info['abstract'] = '\n\n'.join(
                [r.text for r in line.find_all('p')])

    if info:
        info_list.append(info)
        info = {}

    df = pd.DataFrame(info_list)
    print(df.info())

    output_path = 'sigir2022.tsv'
    df[['title', 'authors', 'session', 'url', 'abstract']].to_csv(
        output_path, sep='\t', index=False)
    print('output saved to {}'.format(output_path))


if __name__ == '__main__':
    main()
