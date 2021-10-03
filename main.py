#this program runs from Linux terminal using the following syntax:
#python main.py inputfile
#inputfile is the filename of the initial configuration of the ecosystem
from Ecosystem_DAVID_IONITA_MATT_COMPTON import Ecosystem
from River import River

import sys


def main():
    if len(sys.argv) != 2:
        inputfile = input("Name of input file: ")
    else:
        # Pick up the command line argument
        inputfile = sys.argv[1]
    print(inputfile)

    yn = True if input("Output HTML? (y/N)") == "y" else False

    ecosystem = Ecosystem(inputfile, yn)
    river = River(ecosystem, 11)
    river.run()

main()
