#!/usr/bin/env python3

"""
Download Incidence Matrices from www.hippo.iee.uz.zgora.pl.
"""

from pathlib import Path

import requests
from bs4 import BeautifulSoup


def main():
    base_url = "http://www.hippo.iie.uz.zgora.pl/index.php?v=g&s=n_a&site="
    soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    number_pages = int(soup.find_all('a')[-2].text)
    for page in range(1, number_pages + 1):
        soup = BeautifulSoup(requests.get(base_url + str(page)).content, 'html.parser')
        for img in soup.find_all('img'):
            model = Path(img['src']).stem
            print("Downloading: {}".format(model))
            matrix_url = "http://www.hippo.iie.uz.zgora.pl/download.php?file=pnh/{}.pnh".format(model)
            open('{}.pnh'.format(model), 'wb').write(requests.get(matrix_url, allow_redirects=True).content)


if __name__=='__main__':
    main()
