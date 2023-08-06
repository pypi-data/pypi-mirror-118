#!/usr/bin/env python

import sys
from . import main

if __name__ == '__main__':
    sys.argv[0] = sys.argv[0].replace('__main__.py', 'happyci')
    main()
