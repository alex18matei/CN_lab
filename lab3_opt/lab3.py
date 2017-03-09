import sys
import matrix

if __name__ == '__main__':
    if sys.argv[-1] == 'nogui':
        matrix.nogui()
    else:
        matrix.gui()
