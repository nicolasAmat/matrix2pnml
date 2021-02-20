#!/usr/bin/env python3

"""
matrix2pnml

Input file: incidence matrix

> Number of columns
> Number of rows
> Matrix: Columns represent places and rows represent transitions of the net, last
line of the matrix is the initial marking:
- a `1` in the matrix indicates that post(p,t)=1
- a `x` in the matrix indicates that pre(p,t)=1
"""

import argparse
import subprocess
from pathlib import Path


def main():
    # Arguments parser
    parser = argparse.ArgumentParser(description='matrix2pnml')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 1.0.0',
                        help='show the version number and exit')

    parser.add_argument('infile',
                        metavar='filename',
                        type=str,
                        help='input Petri net (.pnml format)')

    results = parser.parse_args()

    # Read incidence matrix (.pnh format) and write the corresponding Petri net (.net format) 
    with open(results.infile, 'r') as fp_matrix, open(results.infile.replace('.pnh', '.net'), 'w') as fp_net:

        # Read incidence matrix
        matrix = fp_matrix.read().splitlines()

        # Get number of columns and rows
        columns = int(matrix.pop(0))
        rows = int(matrix.pop(0))

        # Write net name
        fp_net.write("net {{{}}}\n".format(Path(results.infile).stem))    

        # Write transitions
        for transition, row in enumerate(matrix[:rows - 1]):
            input_places, output_places = [], []
            for place, value in enumerate(row):
                if value == 'x':
                    input_places.append(place)
                if value == '1':
                    output_places.append(place)
            if input_places or output_places:
                fp_net.write("tr t{}  {} -> {}\n".format(transition, ' '.join(map(lambda pl: "p{}".format(pl), input_places)), ' '.join(map(lambda pl: "p{}".format(pl), output_places))))
                  
        # Write initial marking
        for place, value in enumerate(matrix[rows - 1]):
            if value == '1':
                fp_net.write('pl p{} (1)\n'.format(place))

    # Convert from .net to .pnml
    subprocess.run(['ndrio', results.infile.replace('.pnh', '.net'), results.infile.replace('.pnh', '.pnml')])


if __name__=='__main__':
    main()
