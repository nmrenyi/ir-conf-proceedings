"""
script of parsing the paper list of SIGIR 2022 from https://sigir.org/sigir2022/program/proceedings/
"""
from bs4 import BeautifulSoup

with open('raw-page/sigir2022.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

all_papers = soup.find(id='DLcontent')

