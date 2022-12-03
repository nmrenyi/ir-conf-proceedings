"""
script of parsing the paper list of theWebConf 2022 from https://www2022.thewebconf.org/main-proceedings/
"""
from bs4 import BeautifulSoup


def main():
    with open('www2022.html', 'r') as f:
        html_page = f.read()
    soup = BeautifulSoup(html_page, 'html.parser')

    proceeding = soup.find(id='DLcontent')
    for track in proceeding.find_all('details'):
        pass


if __name__ == '__main__':
    main()
