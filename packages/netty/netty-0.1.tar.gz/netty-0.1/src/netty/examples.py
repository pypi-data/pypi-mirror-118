from netty import connection
import sys, os

ver = int(sys.version.split("(")[0].split(".")[0])
def runexample(file):
    try:
        filename = str(file) + "-simple.py"
        if ver == 3:
            cwd = os.getcwd()
            os.system('python ' + 'examples/' + filename)
        elif ver ==  2:
            os.system('python3 ' + 'examples/' + filename)

    except FileNotFoundError:
        print('That example doesn\'t exist!')
