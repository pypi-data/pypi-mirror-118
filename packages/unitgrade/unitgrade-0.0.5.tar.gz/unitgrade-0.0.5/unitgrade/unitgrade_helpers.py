import numpy as np
from tabulate import tabulate
from datetime import datetime
import pickle
import pyfiglet
import unitgrade
from unitgrade import Hidden, myround, msum, mfloor
from unitgrade import __version__

# from unitgrade.unitgrade import Hidden
# import unitgrade as ug
# import unitgrade.unitgrade as ug
import inspect
import os
import argparse


parser = argparse.ArgumentParser(description='Evaluate your report.', epilog="""Example: 
To run all tests in a report: 

> python report1.py

To run only question 2 or question 2.1

> python report1.py -q 2
> python report1.py -q 2.1

Note this scripts does not grade your report. To grade your report, use:

> python report1_grade.py

Finally, note that if your report is part of a module (package), and the report script requires part of that package, the -m option for python may be useful.
As an example, suppose the report file is Documents/course_package/report1.py, and `course_package` is a python package. Change directory to 'Documents/` and execute:

> python -m course_package.report1

see https://docs.python.org/3.9/using/cmdline.html
""", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-q', nargs='?', type=str, default=None, help='Only evaluate this question (example: -q 2)')
parser.add_argument('--showexpected',  action="store_true",  help='Show the expected/desired result')
parser.add_argument('--showcomputed',  action="store_true",  help='Show the answer your code computes')
parser.add_argument('--unmute',  action="store_true",  help='Show result of print(...) commands in code')
parser.add_argument('--passall',  action="store_true",  help='Automatically pass all tests. Useful when debugging.')

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')



def evaluate_report_student(report, question=None, qitem=None):
    args = parser.parse_args()
    if question is None and args.q is not None:
        question = args.q
        if "." in question:
            question, qitem = [int(v) for v in question.split(".")]
        else:
            question = int(question)

    # print(args)
    results, table_data = evaluate_report(report, question=question, qitem=qitem, verbose=False, passall=args.passall, show_expected=args.showexpected, show_computed=args.showcomputed,unmute=args.unmute)

    if question is None:
        print("Provisional evaluation")
        tabulate(table_data)
        table = table_data
        print(tabulate(table))
        print(" ")
    print("Note your results have not yet been registered. \nTo register your results, please run the file:")

    fr = inspect.getouterframes(inspect.currentframe())[1].filename
    print(">>>", os.path.basename(fr)[:-3] + "_grade.py")
    print("In the same manner as you ran this file.")
    return results


def upack(q):
    # h = zip([(i['w'], i['possible'], i['obtained']) for i in q.values()])
    h =[(i['w'], i['possible'], i['obtained']) for i in q.values()]
    h = np.asarray(h)
    return h[:,0], h[:,1], h[:,2],
    #
    # ws, possible, obtained = (np.asarray(x).squeeze() for x in zip([(i['w'], i['possible'], i['obtained']) for i in q.values()]))
    # return ws, possible, obtained

def evaluate_report(report, question=None, qitem=None, passall=False, verbose=False,  show_expected=False, show_computed=False,unmute=False):
    now = datetime.now()
    # show_expected = True
    ascii_banner = pyfiglet.figlet_format("UnitGrade", font="doom")
    b = "\n".join( [l for l in ascii_banner.splitlines() if len(l.strip()) > 0] )
    print(b + " v" + __version__)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Started: " + dt_string)
    print("Evaluating " + report.title, "(use --help for options)")
    print(f"Loaded answers from: ", report.computed_answers_file, "\n")
    table_data = []
    nL = 80

    score = {}
    for n, (q, w) in enumerate(report.questions):
        q_hidden = issubclass(q.__class__, Hidden)
        if question is not None and n+1 != question:
            continue

        print(f"Question {n+1}: {q.title}")
        print("="*nL)
        q.possible = 0
        q.obtained = 0

        q_ = {} # Gather score in this class.
        for j, (item, iw) in enumerate(q.items):
            if qitem is not None and question is not None and item is not None and j+1 != qitem:
                continue

            ss = f"*** q{n+1}.{j+1}) {item.title}"
            el = nL-4
            if len(ss) < el:
                ss += '.'*(el-len(ss))
            hidden = issubclass(item.__class__, Hidden)
            if not hidden:
                print(ss, end="")
            (current, possible) = item.get_points(show_expected=show_expected, show_computed=show_computed,unmute=unmute, passall=passall)
            q_[j] = {'w': iw, 'possible': possible, 'obtained': current, 'hidden': hidden}
            # q.possible += possible * iw
            # q.obtained += current * iw
            if not hidden:
                if current == possible:
                    print(f"PASS")
                else:
                    print(f"*** FAILED")

        ws, possible, obtained = upack(q_)
        possible = int(ws @ possible)
        obtained = int(ws @ obtained)
        obtained = int(myround(int((w * obtained) / possible ))) if possible > 0 else 0
        score[n] = {'w': w, 'possible': w, 'obtained': obtained, 'ítems': q_, 'hidden': q_hidden}

        q.obtained = obtained
        q.possible = possible

        s1 = f"*** Question q{n+1}"
        s2 = f" {q.obtained}/{w}"
        print(s1 + ("."* (nL-len(s1)-len(s2) )) + s2 )
        print(" ")
        table_data.append([f"Question q{n+1}", f"{q.obtained}/{w}"])

    ws, possible, obtained = upack(score)
    possible = int( msum(possible) )
    obtained = int( msum(obtained) ) # Cast to python int
    report.possible = possible
    report.obtained = obtained
    now = datetime.now()
    dt_string = now.strftime("%H:%M:%S")
    print(f"Completed: "+ dt_string)
    table_data.append(["Total", ""+str(report.obtained)+"/"+str(report.possible) ])
    results = {'total': (obtained, possible), 'details': score}
    return results, table_data
