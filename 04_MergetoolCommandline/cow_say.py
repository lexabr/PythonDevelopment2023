import cowsay
import cmd
import shlex


optionals_map = {
    '-c': 'cow',
    '-e': 'eyes',
    '-T': 'tongue'
}


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
        opts_to_pass = {
            '-c': 'default',
            '-e': cowsay.Option.eyes,
            '-T': cowsay.Option.tongue
        }
        for op, val in zip(optional[::2], optional[1::2]):
            opts_to_pass[op] = val
        opts_to_pass = {optionals_map[op]: val for op, val in opts_to_pass.items()}
        print(cowsay.cowsay(message, **opts_to_pass))


    def do_exit(self, args):
        '''Stop running cowsay cmd'''
        return True
    

if __name__ == '__main__':

    CowsayInteractive().cmdloop()