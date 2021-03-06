import argparse
import os
import sys
import re


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_dir',
        required=True,
        type=str
    )
    parser.add_argument(
        '--output_dir',
        required=True,
        type=str
    )
    return vars(parser.parse_args(sys.argv[1:]))


def split_line(line):
    return [line[0], ' '.join(line[1:])]


def remove_commas(input_filename, output_filename):
    with open(input_filename) as inf:
        with open(output_filename, 'w') as ouf:
            for line in inf.readlines():
                out_line = remove_commas_line(line)
                ouf.write(out_line)


def remove_commas_line(line: str):
    return re.sub("[.,]", "", line)


def run(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for p, d, f in os.walk(input_dir):
        output_dirpath = os.path.join(output_dir, os.path.relpath(p, input_dir))
        print(output_dirpath)
        if not os.path.exists(output_dirpath):
            os.mkdir(output_dirpath)
        for filename in f:
            if os.path.splitext(filename)[1] == '.txt':
                input_filename = os.path.join(p, filename)
                output_filename = os.path.join(output_dirpath, filename)
                if not os.path.exists(output_filename):
                    remove_commas(input_filename, output_filename)


if __name__ == '__main__':
    run(**parse())
