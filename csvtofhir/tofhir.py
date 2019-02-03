import sys
import argparse
import os.path

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.errror("THe file %s does not exist!" %arg)
    else:
        return open(arg, 'r') # return an open file handle

parser = argparse.ArgumentParser(description= 'csv to fhir resources', usage='csvtofhir [-h] [--]')
parser.add_argument('-input', dest='filename', required=True, help = 'input csv or excel file containing data', metavar='FILE')

def main():
    args = parser.parse_args()

if __name__== "__main__":
    main()

