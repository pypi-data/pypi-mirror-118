"""
git add . && git commit -m "Options" && git push &&  pip install git+ssh://git@gitlab.compute.dtu.dk/tuhe/unitgrade.git --upgrade

"""
from . import cache_read
import unittest
import numpy as np
import os
from io import StringIO
import sys
import collections
import inspect

myround = lambda x: np.round(x)  # required.
msum = lambda x: sum(x)
mfloor = lambda x: np.floor(x)

def setup_dir_by_class(C,base_dir):
    name = C.__class__.__name__
    # base_dir = os.path.join(base_dir, name)
    # if not os.path.isdir(base_dir):
    #     os.makedirs(base_dir)
    return base_dir, name

class Hidden:
    def hide(self):
        return True

import sys

class Logger(object):
    def __init__(self, buffer):
        self.terminal = sys.stdout
        self.log = buffer

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        pass

# sys.stdout = Logger()

class Capturing(list):
    def __init__(self, *args, unmute=False, **kwargs):
        self.unmute = unmute
        super().__init__(*args, **kwargs)

    def __enter__(self, capture_errors=True): # don't put arguments here.
        self._stdout = sys.stdout
        self._stringio = StringIO()
        if self.unmute:
            sys.stdout = Logger(self._stringio)
        else:
            sys.stdout = self._stringio

        if capture_errors:
            self._sterr = sys.stderr
            sys.sterr = StringIO() # memory hole it
        self.capture_errors = capture_errors
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
        if self.capture_errors:
            sys.sterr = self._sterr


class QItem(unittest.TestCase):
    title = None
    testfun = unittest.TestCase.assertEqual
    tol = 0

    def __init__(self, working_directory=None, correct_answer_payload=None, *args, **kwargs):
        self.name = self.__class__.__name__
        self._correct_answer_payload = correct_answer_payload
        super().__init__(*args, **kwargs)
        if self.title is None:
            self.title = self.name

    def assertL2(self, computed, expected, tol=None):
        if tol == None:
            tol = self.tol
        diff = np.abs( (np.asarray(computed) - np.asarray(expected)) )
        if np.max(diff) > tol:
            print("Not equal within tolerance {tol}")
            print(f"Element-wise differences {diff.tolist()}")
            self.assertEqual(computed, expected, msg=f"Not equal within tolerance {tol}")

    def assertL2Relative(self, computed, expected, tol=None):
        if tol == None:
            tol = self.tol
        diff = np.abs( (np.asarray(computed) - np.asarray(expected)) )
        diff = diff / (1e-8 + np.abs( (np.asarray(computed) + np.asarray(expected)) ) )
        if np.sum(diff > tol) > 0:
            print(f"Not equal within tolerance {tol}")
            print(f"Element-wise differences {diff.tolist()}")
            self.assertEqual(computed, expected, msg=f"Not equal within tolerance {tol}")

    def compute_answer(self, unmute=False):
        raise NotImplementedError("test code here")

    def test(self, computed, expected):
        self.testfun(computed, expected)

    def get_points(self, verbose=False, show_expected=False, show_computed=False,unmute=False, passall=False, **kwargs):
        possible = 1
        computed = None
        def show_computed_(computed):
            print(">>> Your output:")
            print(computed)

        def show_expected_(expected):
            print(">>> Expected output:")
            print(expected)

        try:
            if unmute:
                print("\n")
            computed = self.compute_answer(unmute=unmute)
        except Exception as e:
            if not passall:
                print("\n=================================================================================")
                print(f"When trying to run test class '{self.name}' your code threw an error:")
                print(e)
                print("=================================================================================")
                import traceback
                traceback.print_exc()
                return (0, possible)
        correct = self._correct_answer_payload
        if show_expected or show_computed:
            print("\n")
        if show_expected:
            show_expected_(correct)
        if show_computed:
            show_computed_(computed)
        try:
            # print(computed, correct)
            # if passall:
            #     computed = correct
            if not passall:
                self.test(computed=computed, expected=correct)
        except Exception as e:
            print("\n=================================================================================")
            print(f"Test output from test class '{self.name}' does not match expected result. Test error:")
            print(e)
            show_computed_(computed)
            show_expected_(correct)
            # print("-------------------------Your output:--------------------------------------------")
            # print(computed)
            # print("-------------------------Expected output:----------------------------------------")
            # print(correct)
            # print("=================================================================================")
            return (0, possible)
        return (1, possible)

    def score(self):
        try:
            self.test()
        except Exception as e:
            return 0
        return 1

class QPrintItem(QItem):
    def compute_answer_print(self):
        """
        Generate output which is to be tested. By default, both text written to the terminal using print(...) as well as return values
        are send to process_output (see compute_answer below). In other words, the text generated is:

        res = compute_Answer_print()
        txt = (any terminal output generated above)
        numbers = (any numbers found in terminal-output txt)

        self.test(process_output(res, txt, numbers), <expected result>)

        :return: Optional values for comparison
        """
        raise Exception("Generate output here. The output is passed to self.process_output")

    def process_output(self, res, txt, numbers):
        return (res, txt)

    def compute_answer(self, unmute=False):
        with Capturing(unmute=unmute) as output:
            res = self.compute_answer_print()
        s = "\n".join(output)
        numbers = extract_numbers(s)
        return self.process_output(res, s, numbers)

class OrderedClassMembers(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()
    def __new__(self, name, bases, classdict):
        classdict['__ordered__'] = [key for key in classdict.keys() if key not in ('__module__', '__qualname__')]
        return type.__new__(self, name, bases, classdict)

class QuestionGroup(metaclass=OrderedClassMembers):
    title = "Graph search"
    items = None
    partially_scored = False

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        if self.items is None:
            self.items = []
            members = [gt for gt in [getattr(self, gt) for gt in self.__ordered__] if inspect.isclass(gt) and issubclass(gt, QItem)]
            for gt in members:
                self.items.append( (gt, 1) )
        self.items = [(I(), w) for I, w in self.items]

class Report():
    title = "report title"
    questions = []
    pack_imports = []

    def __init__(self, strict=False,payload=None):
        working_directory = os.path.abspath(os.path.dirname(inspect.getfile(type(self))))
        # working_directory = os.path.join(pathlib.Path(__file__).parent.absolute(), "payloads/")
        self.wdir, self.name = setup_dir_by_class(self, working_directory)
        self.computed_answers_file = os.path.join(self.wdir, self.name + "_resources_do_not_hand_in.dat")
        self.questions = [(Q(working_directory=self.wdir),w) for Q,w in self.questions]
        # self.strict = strict
        if payload is not None:
            self.set_payload(payload, strict=strict)
        else:
            if os.path.isfile(self.computed_answers_file):
                self.set_payload(cache_read(self.computed_answers_file), strict=strict)
            else:
                s = f"> Warning: The pre-computed answer file, {os.path.abspath(self.computed_answers_file)} is missing. The framework will NOT work as intended. Reasons may be a broken local installation."
                if strict:
                    raise Exception(s)
                else:
                    print(s)

    def set_payload(self, payloads, strict=False):
        for q, _ in self.questions:
            for item, _ in q.items:
                if q.name not in payloads or item.name not in payloads[q.name]:
                    s = f"> Broken resource dictionary submitted to unitgrade for question {q.name} and subquestion {item.name}. Framework will not work."
                    if strict:
                        raise Exception(s)
                    else:
                        print(s)
                item._correct_answer_payload = payloads[q.name][item.name]['payload']

def extract_numbers(txt):
    import re
    numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    all = rx.findall(txt)
    all = [float(a) if '.' in a else int(a) for a in all]
    return all
