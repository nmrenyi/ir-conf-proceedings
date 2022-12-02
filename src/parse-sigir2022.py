"""
script of parsing the paper list of SIGIR 2022 from https://sigir.org/sigir2022/program/proceedings/
"""
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import trange


def append_paper(paper_list, paper):
    paper_list.append(paper)
    return paper_list


with open('raw-page/sigir2022.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

all_papers = soup.find(id='DLcontent')

info_list = []
info = {}
session_name = ''

for i in trange(len(all_papers)):
    line = all_papers.contents[i]
    if line.name == 'h2':
        if info:
            info['session'] = session_name
            info_list = append_paper(info_list, info)
            info = {}
            session_name = ''
        session_name = line.text
    elif line.name == 'h3':
        if info:
            info['session'] = session_name
            info_list = append_paper(info_list, info)
            info = {}
        info['title'] = line.text
        info['url'] = line.find('a').get('href')
    elif line.name == 'ul':
        info['authors'] = line.find('li').text
    elif line.name == 'div':
        info['abstract'] = '\n\n'.join([r.text for r in line.find_all('p')])
if info:
    info_list.append(info)
    info = {}
df = pd.DataFrame(info_list)
print(df.info())
output_path = 'sigir2022.tsv'
df[['title', 'authors', 'session', 'url', 'abstract']].to_csv(
    output_path, sep='\t', index=False)
print('output saved to {}'.format(output_path))
