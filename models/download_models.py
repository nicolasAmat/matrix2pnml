#!/usr/bin/env python3

"""
Download Incidence Matrices from www.hippo.iee.uz.zgora.pl.
"""

from pathlib import Path

import requests
from bs4 import BeautifulSoup


def main():
    base_url = "http://www.hippo.iee.uz.zgora.pl/index.php?v=g&s=n_a&site="

    for page in range(1,11):
        soup = BeautifulSoup(requests.get(base_url + str(page)).content, 'html.parser')
        for img in soup.find_all('img'):
            model = Path(img['src']).stem
            print("Downloading: {}".format(model))
            matrix_url = "http://www.hippo.iee.uz.zgora.pl/download.php?file=pnh/{}.pnh".format(model)
            open('{}.pnh'.format(model), 'wb').write(requests.get(matrix_url, allow_redirects=True).content)


if __name__=='__main__':
    main()
