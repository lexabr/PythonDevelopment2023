import argparse


parser = argparse.ArgumentParser(description='cowsay prog')
parser.add_argument('-e', type=str, default='oo')
parser.add_argument('-f', type=str)
parser.add_argument('-l', action='store_true')
parser.add_argument('-n', action='store_true')
parser.add_argument('-T', type=str, default='  ')
parser.add_argument('-W', type=int, default=40)

# modes options
for opt in 'bdgpstwy':
    parser.add_argument(f'-{opt}', action='store_true')

# message
parser.add_argument('message', nargs='?', default=None)

args = parser.parse_args()