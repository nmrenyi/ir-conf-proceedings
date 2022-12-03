"""
script of parsing the paper list of theWebConf 2022 from https://www2022.thewebconf.org/main-proceedings/
"""
import argparse

import pandas as pd
from bs4 import BeautifulSoup


def parse_track(track):
    track_name = track.find('summary').text
    return []


def parse_proceeding(proceeding):
    info_list = []
    for track in proceeding.find_all('details'):
        track_list = parse_track(track)
        info_list.extend(track_list)
    return info_list


def main():
    with open('www2022.html', 'r') as f:
        html_page = f.read()
    soup = BeautifulSoup(html_page, 'html.parser')

    proceeding = soup.find(id='DLcontent')

    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='tsv',
                        help='output file type (default: tsv, options: tsv, md)')
    args = parser.parse_args()

    info_list = parse_proceeding(proceeding)
    df = pd.DataFrame(info_list)[
        ['title', 'authors', 'session', 'url', 'abstract']]
    print(df.info())

    file_type = args.type
    output_path = '../data/{0}/thewebconf2022.{0}'.format(file_type)

    if file_type == 'tsv':
        df.to_csv(output_path, sep='\t', index=False)
    elif file_type == 'md':
        with open(output_path, 'w') as f:
            f.write(df[['title', 'authors', 'session', 'abstract', 'url']].to_markdown(
                index=False).replace('   ', ''))  # remove redundant whitespace to shrink the file size
    else:
        raise ValueError('Unsupported file type: {}'.format(file_type))
    print('output saved to {}'.format(output_path))


if __name__ == '__main__':
    main()
