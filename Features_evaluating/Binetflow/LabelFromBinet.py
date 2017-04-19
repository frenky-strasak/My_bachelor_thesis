"""
Take labels from binetflows file and then label conn.log
Usage:
python LabelFromBinet.py c:\Users\frenk\Documents\Skola\Bachelor_thesis\datasets\Experiment_1
"""

import sys
import MakeLabel

if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
        
        MakeLabel.take_label_from_binet_flow(path)