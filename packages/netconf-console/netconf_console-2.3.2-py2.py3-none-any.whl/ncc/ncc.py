#!/usr/bin/env python

from __future__ import print_function

import os
import sys


def main():
    print('The package `netconf-console` has been deprecated.'
          ' Please use `netconf-console2` instead.')
    args = sys.argv[:]
    args[0] = os.path.join(os.path.dirname(args[0]), 'netconf-console2')
    os.execv(args[0], args)


if __name__ == "__main__":
    sys.exit(main())
