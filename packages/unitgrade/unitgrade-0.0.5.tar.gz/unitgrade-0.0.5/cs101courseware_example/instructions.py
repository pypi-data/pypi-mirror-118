import os
import textwrap

def fprint(s):
    print("\n".join(textwrap.wrap(s, width=100)))

def tprint(s):
    print(f"\n> {s}\n")

s = """
This is an example script to illustrate unitgrade for a very simple, fictitious course. Because this is a build-in example, 
the source code will likely reside in your site-packages directory. The full example can be found at:"""
fprint(s)
wdir = os.path.dirname(__file__)
tprint(wdir)
print("The directory contains the source for a fictitious course. The content of the directory is:")
for d in os.listdir(wdir):
    if "__" not in d and d != "instructions.py":
        print("> ", d)
print("")
fprint("The file homework1.py is the file you edit as part of the course; you are welcome to open it and inspect the content, but right now it consists of some simple programming tasks plus instructions.")
fprint("The file cs101report1.py contains the actual tests of the program. All the tests are easily readable and the script will work with your debugger if you are using pycharm, however, we will run the script for the command line. ")
fprint("To do so, open a console, and change directory to the cs101 main directory using e.g.:")
tprint(f'cd "{wdir}"')
print("Then run the script as usual")
tprint(f'python cs101report1.py')
fprint("This will run all tests and print how many points you will currently obtain. In this case you should get 18 points out of 18 possible. Once you are happy with the results, run the tamper-proof script:")
tprint(f'python cs101report1_grade.py')
fprint("This will run the same set of tests, but the script has been modified to prevent easy manipulation. You should in other words get the exact same results as before.")
fprint("The script will also generate a submission+file. The submission-file contains the details of the test and we will use it for the evaluation. The file is named:")
tprint('Report0_handin_18_of_18.token')
fprint("This file, and this file alone, is all you should upload. Note the file name contains the number of points obtained.")
