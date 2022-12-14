"""
script of parsing the paper list of theWebConf 2022 from https://www2022.thewebconf.org/main-proceedings/
"""
import argparse

import pandas as pd
from bs4 import BeautifulSoup

from utils import parse_args, parse_html, save_file


def parse_track(track):
    track_name = track.find('summary').text
    title_list = [x.text for x in track.find_all('a')]
    url_list = [x.get('href') for x in track.find_all('a')]
    author_list = []
    for names in track.find_all('ul'):
        authors = []
        for name in names.find_all('li'):
            authors.append(name.text)
        author_list.append(', '.join(authors))
    abstract_list = []
    for abstract_paras in track.findAll('div', {'class': 'DLabstract'}):
        abstract = []
        for para in abstract_paras:
            abstract.append(para.text.strip())
        abstract_list.append('\n\n'.join(abstract))
    assert (len(title_list) == len(url_list) ==
            len(author_list) == len(abstract_list))
    return [{'title': title_list[i], 'authors': author_list[i], 'session': track_name, 'abstract': abstract_list[i], 'url': url_list[i]} for i in range(len(title_list))]


def parse_proceeding(proceeding):
    info_list = []
    for track in proceeding.find_all('details'):
        track_list = parse_track(track)
        info_list.extend(track_list)
    return info_list


def main():
    proceeding = parse_html(
        url='https://www2022.thewebconf.org/main-proceedings/', target_id='DLcontent')

    args = parse_args()

    info_list = parse_proceeding(proceeding)
    df = pd.DataFrame(info_list)[
        ['title', 'authors', 'session', 'url', 'abstract']]
    print(df.info())

    file_type = args.type
    output_path = '../data/{0}/thewebconf2022.{0}'.format(file_type)

    save_file(df, output_path, file_type)


if __name__ == '__main__':
    main()
