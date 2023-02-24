import argparse
from cowsay import cowsay, list_cows


def call_cow(args):
    if args.l:
        cow_words = list_cows()
        print(cow_words)
    else:
        preset=None
        preset_kwargs = vars(args)
        for p in 'bdgpstwy':
            if preset_kwargs[p]:
                preset=p
                break

        cow_words = cowsay(message=args.message, cow=args.f, preset=preset, eyes=args.e[:2],
                           tongue=args.T[:2], width=args.W, wrap_text=not args.n)
        print(cow_words)



parser = argparse.ArgumentParser(description='cowsay prog')
parser.add_argument('-e', type=str, default='oo')
parser.add_argument('-f', type=str, default='default')
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

# call cowsay
call_cow(args)