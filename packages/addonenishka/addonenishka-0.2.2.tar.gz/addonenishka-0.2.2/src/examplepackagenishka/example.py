import argparse
import pandas as pd
import numpy as np
import os

def list_files(startpath):
    for root, _, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

class addone(object):

    number = 0
    def __init__(self, **kw):
        self.number = kw['number']

    def addtest(self):
        print(self.number + 1)
        print('Random numpy integer: ' + str(np.random.randint(4)))
        sample_df = pd.DataFrame(pd.read_csv('data/sample_data.csv'))
        print(list_files(''))
        print(sample_df.to_markdown())

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-number', type=int, help='input number', default=0)
    args = parser.parse_args()
    
    obj = addone(number=args.number)
    obj.addtest()
