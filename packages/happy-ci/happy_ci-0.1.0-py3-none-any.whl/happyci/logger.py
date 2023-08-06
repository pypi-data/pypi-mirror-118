
import sys


def debug(*message):
    print(*message, sep=' ')


def fail(*message):
    print('Failed', *message, sep=' ', file=sys.stderr)

