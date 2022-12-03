from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def parse_html(url, target_id):
    print('Requesting data... (from {})'.format(url))
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    print('Parsing data...')
    soup = BeautifulSoup(html_page, 'html.parser')
    return soup.find(id=target_id)


def save_file(df, output_path, file_type):
    if file_type == 'tsv':
        df.to_csv(output_path, sep='\t', index=False)
    elif file_type == 'md':
        with open(output_path, 'w') as f:
            f.write(df[['title', 'authors', 'session', 'abstract', 'url']].to_markdown(
                index=False).replace('   ', ''))  # remove redundant whitespace to shrink the file size
    else:
        raise ValueError('Unsupported file type: {}'.format(file_type))
    print('output saved to {}'.format(output_path))
