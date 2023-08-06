import argparse
import pandas as pd
import numpy as np
import os
import pkgutil
from io import BytesIO

class addone(object):

    number = 0
    def __init__(self, **kw):
        self.number = kw['number']

    def addtest(self):
        print(self.number + 1)
        print('Random numpy integer: ' + str(np.random.randint(4)))
        data = pkgutil.get_data(__name__, 'data/sample_data.csv')
        print(data)
        sample_df = pd.DataFrame(pd.read_csv(BytesIO(data)))
        print(sample_df.to_markdown())

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-number', type=int, help='input number', default=0)
    args = parser.parse_args()
    
    obj = addone(number=args.number)
    obj.addtest()
