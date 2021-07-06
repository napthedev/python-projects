import os
import getpass

USER = getpass.getuser()
PATH = r"C:\Users\{}\AppData\Roaming\Sublime Text\Packages\User\.SublimeREPLHistory\python.db".format(USER)

if os.path.exists(PATH):
    os.remove(PATH)
    print("Sublime REPL fixed")
else:
    print("Sublime REPL has already been fixed")
