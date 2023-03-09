import cowsay
import cmd
import shlex


optionals_map = {
    '-c': 'cow',
    '-e': 'eyes',
    '-T': 'tongue',
    '-b': 'brackets',
    '-l': 'width',
    '-w': 'wrap_text'
}

cow_opts_to_pass = {
    '-c': 'default',
    '-e': cowsay.Option.eyes,
    '-T': cowsay.Option.tongue
}

bubble_opts_to_pass = {
    '-b': cowsay.THOUGHT_OPTIONS['cowsay'],
    '-l': 40,
    '-w': True
}


def extract_ops(optional, opts_to_pass):
    for op, val in zip(optional[::2], optional[1::2]):
        opts_to_pass[op] = cowsay.THOUGHT_OPTIONS[val] if op == '-b' else val
        if op == '-l':
            opts_to_pass[op] = int(val)
    return {optionals_map[op]: val for op, val in opts_to_pass.items()}


class CowsayInteractive(cmd.Cmd):
    prompt = 'type command > '


    def do_list_cows(self, args):
        '''
        Prints all possible cow files names in the given directory
        If directory is empty then prints default cow files names
        '''
        if len(shlex.split(args)) > 0:
            print(*cowsay.list_cows(shlex.split(args)[0]))
        else:
            print(*cowsay.list_cows())


    def do_cowsay(self, args):
        '''
        Prints cowsay string with given message and parameters
        Usage: cowsay message [-c cow] [-e eye] [-T tongue]

        message: string excpected to be cowsaid
        cow: -c name of cow file
        eye: -e custom eye string
        tongue: -T custom tongue string
        '''

        message, *optional = shlex.split(args)
        opts_to_pass = extract_ops(optional, cow_opts_to_pass)
        print(cowsay.cowsay(message, **opts_to_pass))

    
    def do_cowthink(self, args):
        '''
        Prints cowthink string with given message and parameters
        Usage: cowthink message [-c cow] [-e eye] [-T tongue]

        message: string excpected to be cowsaid
        cow: -c name of cow file
        eye: -e custom eye string
        tongue: -T custom tongue string
        '''

        message, *optional = shlex.split(args)
        opts_to_pass = extract_ops(optional, cow_opts_to_pass)
        print(cowsay.cowthink(message, **opts_to_pass))

    
    def do_make_bubble(self, args):
        '''
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        Usage: make_bubble text [-b brackets] [-d width] [-w wrap_text]

        text: string expected to be in bubble
        brackets: -b cowsay or cowthink
        width: -l int
        wrap_text: -w bool, if text should be wrapped
        '''

        message, *optional = shlex.split(args)
        opts_to_pass = extract_ops(optional, bubble_opts_to_pass)
        print(opts_to_pass)
        print(cowsay.make_bubble(message, **opts_to_pass))


    def do_exit(self, args):
        '''Stop running cowsay cmd'''
        return True
    

if __name__ == '__main__':

    CowsayInteractive().cmdloop()