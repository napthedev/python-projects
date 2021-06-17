import os
import getpass

USER = getpass.getuser()
PATH = r"C:\Users\{}\AppData\Roaming\Sublime Text\Packages\User\.SublimeREPLHistory\python.db".format(USER)

os.remove(PATH)
