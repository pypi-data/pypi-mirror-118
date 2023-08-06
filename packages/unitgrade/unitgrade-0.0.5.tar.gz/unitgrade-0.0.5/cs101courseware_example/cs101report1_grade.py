'''WARNING: Modifying, decompiling or otherwise tampering with this script, it's data or the resulting .token file will be investigated as a cheating attempt.'''
import numpy as np
WebLqOFrgMVsHPQuIXjh=str
WebLqOFrgMVsHPQuIXjT=None
WebLqOFrgMVsHPQuIXjn=int
WebLqOFrgMVsHPQuIXjJ=False
WebLqOFrgMVsHPQuIXjl=print
WebLqOFrgMVsHPQuIXjc=len
WebLqOFrgMVsHPQuIXjG=enumerate
WebLqOFrgMVsHPQuIXjy=issubclass
WebLqOFrgMVsHPQuIXjf=getattr
WebLqOFrgMVsHPQuIXjD=open
WebLqOFrgMVsHPQuIXjN=eval
WebLqOFrgMVsHPQuIXjz=globals
WebLqOFrgMVsHPQuIXjR=True
WebLqOFrgMVsHPQuIXjp=np.asarray
from tabulate import tabulate
from datetime import datetime
WebLqOFrgMVsHPQuIXja=datetime.now
import pickle
WebLqOFrgMVsHPQuIXjw=pickle.loads
import pyfiglet
WebLqOFrgMVsHPQuIXjE=pyfiglet.figlet_format
import inspect
WebLqOFrgMVsHPQuIXjk=inspect.currentframe
WebLqOFrgMVsHPQuIXjm=inspect.getouterframes
import os
WebLqOFrgMVsHPQuIXjK=os.getcwd
WebLqOFrgMVsHPQuIXjC=os.path
import argparse
WebLqOFrgMVsHPQuIXjd=argparse.RawTextHelpFormatter
WebLqOFrgMVsHPQuIXjS=argparse.ArgumentParser
WebLqOFrgMVsHPQuIXBj=WebLqOFrgMVsHPQuIXjS(description='Evaluate your report.',epilog="""Example: 
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
""", formatter_class=WebLqOFrgMVsHPQuIXjd)
WebLqOFrgMVsHPQuIXBj.add_argument('-q',nargs='?',type=WebLqOFrgMVsHPQuIXjh,default=WebLqOFrgMVsHPQuIXjT,help='Only evaluate this question (example: -q 2)')
WebLqOFrgMVsHPQuIXBj.add_argument('--showexpected',action="store_true",help='Show the expected/desired result')
WebLqOFrgMVsHPQuIXBj.add_argument('--showcomputed',action="store_true",help='Show the answer your code computes')
WebLqOFrgMVsHPQuIXBj.add_argument('--unmute',action="store_true",help='Show result of print(...) commands in code')
WebLqOFrgMVsHPQuIXBj.add_argument('--passall',action="store_true",help='Automatically pass all tests. Useful when debugging.')
def WebLqOFrgMVsHPQuIXBv(WebLqOFrgMVsHPQuIXBG,question=WebLqOFrgMVsHPQuIXjT,qitem=WebLqOFrgMVsHPQuIXjT):
 WebLqOFrgMVsHPQuIXBa=WebLqOFrgMVsHPQuIXBj.parse_args()
 if question is WebLqOFrgMVsHPQuIXjT and WebLqOFrgMVsHPQuIXBa.q is not WebLqOFrgMVsHPQuIXjT:
  question=WebLqOFrgMVsHPQuIXBa.q
  if "." in question:
   question,qitem=[WebLqOFrgMVsHPQuIXjn(v)for v in question.split(".")]
  else:
   question=WebLqOFrgMVsHPQuIXjn(question)
 WebLqOFrgMVsHPQuIXBm,WebLqOFrgMVsHPQuIXBk=WebLqOFrgMVsHPQuIXBo(WebLqOFrgMVsHPQuIXBG,question=question,qitem=qitem,verbose=WebLqOFrgMVsHPQuIXjJ,passall=WebLqOFrgMVsHPQuIXBa.passall,show_expected=WebLqOFrgMVsHPQuIXBa.showexpected,show_computed=WebLqOFrgMVsHPQuIXBa.showcomputed,unmute=WebLqOFrgMVsHPQuIXBa.unmute)
 if question is WebLqOFrgMVsHPQuIXjT:
  WebLqOFrgMVsHPQuIXjl("Provisional evaluation")
  tabulate(WebLqOFrgMVsHPQuIXBk)
  WebLqOFrgMVsHPQuIXBC=WebLqOFrgMVsHPQuIXBk
  WebLqOFrgMVsHPQuIXjl(tabulate(WebLqOFrgMVsHPQuIXBC))
  WebLqOFrgMVsHPQuIXjl(" ")
 WebLqOFrgMVsHPQuIXjl("Note your results have not yet been registered. \nTo register your results, please run the file:")
 fr=WebLqOFrgMVsHPQuIXjm(WebLqOFrgMVsHPQuIXjk())[1].filename
 WebLqOFrgMVsHPQuIXjl(">>>",WebLqOFrgMVsHPQuIXjC.basename(fr)[:-3]+"_grade.py")
 WebLqOFrgMVsHPQuIXjl("In the same manner as you ran this file.")
 return WebLqOFrgMVsHPQuIXBm
def WebLqOFrgMVsHPQuIXBx(q):
 h=[(i['w'],i['possible'],i['obtained'])for i in q.values()]
 h=WebLqOFrgMVsHPQuIXjp(h)
 return h[:,0],h[:,1],h[:,2],
def WebLqOFrgMVsHPQuIXBo(WebLqOFrgMVsHPQuIXBG,question=WebLqOFrgMVsHPQuIXjT,qitem=WebLqOFrgMVsHPQuIXjT,passall=WebLqOFrgMVsHPQuIXjJ,verbose=WebLqOFrgMVsHPQuIXjJ,show_expected=WebLqOFrgMVsHPQuIXjJ,show_computed=WebLqOFrgMVsHPQuIXjJ,unmute=WebLqOFrgMVsHPQuIXjJ):
 WebLqOFrgMVsHPQuIXBK=WebLqOFrgMVsHPQuIXja()
 WebLqOFrgMVsHPQuIXBS=WebLqOFrgMVsHPQuIXjE("UnitGrade",font="doom")
 b="\n".join([l for l in WebLqOFrgMVsHPQuIXBS.splitlines()if WebLqOFrgMVsHPQuIXjc(l.strip())>0])
 WebLqOFrgMVsHPQuIXjl(b+" v"+__version__)
 WebLqOFrgMVsHPQuIXBd=WebLqOFrgMVsHPQuIXBK.strftime("%d/%m/%Y %H:%M:%S")
 WebLqOFrgMVsHPQuIXjl("Started: "+WebLqOFrgMVsHPQuIXBd)
 WebLqOFrgMVsHPQuIXjl("Evaluating "+WebLqOFrgMVsHPQuIXBG.title,"(use --help for options)")
 WebLqOFrgMVsHPQuIXjl(f"Loaded answers from: ",WebLqOFrgMVsHPQuIXBG.computed_answers_file,"\n")
 WebLqOFrgMVsHPQuIXBk=[]
 nL=80
 WebLqOFrgMVsHPQuIXBt={}
 for n,(q,w)in WebLqOFrgMVsHPQuIXjG(WebLqOFrgMVsHPQuIXBG.questions):
  WebLqOFrgMVsHPQuIXBh=WebLqOFrgMVsHPQuIXjy(q.__class__,Hidden)
  if question is not WebLqOFrgMVsHPQuIXjT and n+1!=question:
   continue
  WebLqOFrgMVsHPQuIXjl(f"Question {n+1}: {q.title}")
  WebLqOFrgMVsHPQuIXjl("="*nL)
  q.possible=0
  q.obtained=0
  q_={}
  for j,(item,iw)in WebLqOFrgMVsHPQuIXjG(q.items):
   if qitem is not WebLqOFrgMVsHPQuIXjT and question is not WebLqOFrgMVsHPQuIXjT and item is not WebLqOFrgMVsHPQuIXjT and j+1!=qitem:
    continue
   ss=f"*** q{n+1}.{j+1}) {item.title}"
   el=nL-4
   if WebLqOFrgMVsHPQuIXjc(ss)<el:
    ss+='.'*(el-WebLqOFrgMVsHPQuIXjc(ss))
   WebLqOFrgMVsHPQuIXBT=WebLqOFrgMVsHPQuIXjy(item.__class__,Hidden)
   if not WebLqOFrgMVsHPQuIXBT:
    WebLqOFrgMVsHPQuIXjl(ss,end="")
   (WebLqOFrgMVsHPQuIXBJ,WebLqOFrgMVsHPQuIXBl)=item.get_points(show_expected=show_expected,show_computed=show_computed,unmute=unmute,passall=passall)
   q_[j]={'w':iw,'possible':WebLqOFrgMVsHPQuIXBl,'obtained':WebLqOFrgMVsHPQuIXBJ,'hidden':WebLqOFrgMVsHPQuIXBT}
   if not WebLqOFrgMVsHPQuIXBT:
    if WebLqOFrgMVsHPQuIXBJ==WebLqOFrgMVsHPQuIXBl:
     WebLqOFrgMVsHPQuIXjl(f"PASS")
    else:
     WebLqOFrgMVsHPQuIXjl(f"*** FAILED")
  ws,WebLqOFrgMVsHPQuIXBl,WebLqOFrgMVsHPQuIXBc=WebLqOFrgMVsHPQuIXBx(q_)
  WebLqOFrgMVsHPQuIXBl=WebLqOFrgMVsHPQuIXjn(ws@WebLqOFrgMVsHPQuIXBl)
  WebLqOFrgMVsHPQuIXBc=WebLqOFrgMVsHPQuIXjn(ws@WebLqOFrgMVsHPQuIXBc)
  WebLqOFrgMVsHPQuIXBc=WebLqOFrgMVsHPQuIXjn(myround(WebLqOFrgMVsHPQuIXjn((w*WebLqOFrgMVsHPQuIXBc)/WebLqOFrgMVsHPQuIXBl)))if WebLqOFrgMVsHPQuIXBl>0 else 0
  WebLqOFrgMVsHPQuIXBt[n]={'w':w,'possible':w,'obtained':WebLqOFrgMVsHPQuIXBc,'Ã­tems':q_,'hidden':WebLqOFrgMVsHPQuIXBh}
  q.obtained=WebLqOFrgMVsHPQuIXBc
  q.possible=WebLqOFrgMVsHPQuIXBl
  s1=f"*** Question q{n+1}"
  s2=f" {q.obtained}/{w}"
  WebLqOFrgMVsHPQuIXjl(s1+("."*(nL-WebLqOFrgMVsHPQuIXjc(s1)-WebLqOFrgMVsHPQuIXjc(s2)))+s2)
  WebLqOFrgMVsHPQuIXjl(" ")
  WebLqOFrgMVsHPQuIXBk.append([f"Question q{n+1}",f"{q.obtained}/{w}"])
 ws,WebLqOFrgMVsHPQuIXBl,WebLqOFrgMVsHPQuIXBc=WebLqOFrgMVsHPQuIXBx(WebLqOFrgMVsHPQuIXBt)
 WebLqOFrgMVsHPQuIXBl=WebLqOFrgMVsHPQuIXjn(msum(WebLqOFrgMVsHPQuIXBl))
 WebLqOFrgMVsHPQuIXBc=WebLqOFrgMVsHPQuIXjn(msum(WebLqOFrgMVsHPQuIXBc))
 WebLqOFrgMVsHPQuIXBG.possible=WebLqOFrgMVsHPQuIXBl
 WebLqOFrgMVsHPQuIXBG.obtained=WebLqOFrgMVsHPQuIXBc
 WebLqOFrgMVsHPQuIXBK=WebLqOFrgMVsHPQuIXja()
 WebLqOFrgMVsHPQuIXBd=WebLqOFrgMVsHPQuIXBK.strftime("%H:%M:%S")
 WebLqOFrgMVsHPQuIXjl(f"Completed: "+WebLqOFrgMVsHPQuIXBd)
 WebLqOFrgMVsHPQuIXBk.append(["Total",""+WebLqOFrgMVsHPQuIXjh(WebLqOFrgMVsHPQuIXBG.obtained)+"/"+WebLqOFrgMVsHPQuIXjh(WebLqOFrgMVsHPQuIXBG.possible)])
 WebLqOFrgMVsHPQuIXBm={'total':(WebLqOFrgMVsHPQuIXBc,WebLqOFrgMVsHPQuIXBl),'details':WebLqOFrgMVsHPQuIXBt}
 return WebLqOFrgMVsHPQuIXBm,WebLqOFrgMVsHPQuIXBk
from tabulate import tabulate
from datetime import datetime
WebLqOFrgMVsHPQuIXja=datetime.now
import inspect
WebLqOFrgMVsHPQuIXjk=inspect.currentframe
WebLqOFrgMVsHPQuIXjm=inspect.getouterframes
import json
WebLqOFrgMVsHPQuIXjt=json.dumps
import os
WebLqOFrgMVsHPQuIXjK=os.getcwd
WebLqOFrgMVsHPQuIXjC=os.path
import bz2
import pickle
WebLqOFrgMVsHPQuIXjw=pickle.loads
def WebLqOFrgMVsHPQuIXBA(WebLqOFrgMVsHPQuIXBy,WebLqOFrgMVsHPQuIXBz):
 with WebLqOFrgMVsHPQuIXjf(bz2,'open')(WebLqOFrgMVsHPQuIXBz,"wt")as f:
  f.write(WebLqOFrgMVsHPQuIXBy)
def WebLqOFrgMVsHPQuIXjB(WebLqOFrgMVsHPQuIXBG,output_dir=WebLqOFrgMVsHPQuIXjT):
 n=80
 WebLqOFrgMVsHPQuIXBm,WebLqOFrgMVsHPQuIXBk=WebLqOFrgMVsHPQuIXBo(WebLqOFrgMVsHPQuIXBG)
 WebLqOFrgMVsHPQuIXjl(" ")
 WebLqOFrgMVsHPQuIXjl("="*n)
 WebLqOFrgMVsHPQuIXjl("Final evaluation")
 WebLqOFrgMVsHPQuIXjl(tabulate(WebLqOFrgMVsHPQuIXBk))
 WebLqOFrgMVsHPQuIXBm['sources']={}
 WebLqOFrgMVsHPQuIXjl("Gathering files...")
 for m in WebLqOFrgMVsHPQuIXBG.pack_imports:
  with WebLqOFrgMVsHPQuIXjD(m.__file__,'r')as f:
   WebLqOFrgMVsHPQuIXBm['sources'][m.__name__]=f.read()
  WebLqOFrgMVsHPQuIXjl(f"*** {m.__name__}")
 WebLqOFrgMVsHPQuIXBm['sources']={}
 WebLqOFrgMVsHPQuIXBy=WebLqOFrgMVsHPQuIXjt(WebLqOFrgMVsHPQuIXBm,indent=4)
 if output_dir is WebLqOFrgMVsHPQuIXjT:
  output_dir=WebLqOFrgMVsHPQuIXjK()
 WebLqOFrgMVsHPQuIXBD=WebLqOFrgMVsHPQuIXBG.__class__.__name__+"_handin"
 WebLqOFrgMVsHPQuIXBN,WebLqOFrgMVsHPQuIXBl=WebLqOFrgMVsHPQuIXBm['total']
 WebLqOFrgMVsHPQuIXBz="%s_%i_of_%i.token"%(WebLqOFrgMVsHPQuIXBD,WebLqOFrgMVsHPQuIXBN,WebLqOFrgMVsHPQuIXBl)
 WebLqOFrgMVsHPQuIXBz=WebLqOFrgMVsHPQuIXjC.join(output_dir,WebLqOFrgMVsHPQuIXBz)
 WebLqOFrgMVsHPQuIXBA(WebLqOFrgMVsHPQuIXBy,WebLqOFrgMVsHPQuIXBz)
 WebLqOFrgMVsHPQuIXjl(" ")
 WebLqOFrgMVsHPQuIXjl("To get credit for your results, please upload the single file: ")
 WebLqOFrgMVsHPQuIXjl(">",WebLqOFrgMVsHPQuIXBz)
 WebLqOFrgMVsHPQuIXjl("To campusnet without any modifications.")
def WebLqOFrgMVsHPQuIXjY(WebLqOFrgMVsHPQuIXBi,WebLqOFrgMVsHPQuIXBR,payload):
 WebLqOFrgMVsHPQuIXjN("exec")(WebLqOFrgMVsHPQuIXBR,WebLqOFrgMVsHPQuIXjz())
 pl=WebLqOFrgMVsHPQuIXjw(payload)
 WebLqOFrgMVsHPQuIXBG=WebLqOFrgMVsHPQuIXjN(WebLqOFrgMVsHPQuIXBi)(payload=pl,strict=WebLqOFrgMVsHPQuIXjR)
 return WebLqOFrgMVsHPQuIXBG
WebLqOFrgMVsHPQuIXBR='__version__ = "0.0.5"\nimport os\nimport compress_pickle\n\ndef cache_write(object, file_name, verbose=True):\n    dn = os.path.dirname(file_name)\n    if not os.path.exists(dn):\n        os.mkdir(dn)\n    if verbose: print("Writing cache...", file_name)\n    with open(file_name, \'wb\', ) as f:\n        compress_pickle.dump(object, f, compression="lzma")\n    if verbose: print("Done!")\n\n\ndef cache_exists(file_name):\n    # file_name = cn_(file_name) if cache_prefix else file_name\n    return os.path.exists(file_name)\n\n\ndef cache_read(file_name):\n    # file_name = cn_(file_name) if cache_prefix else file_name\n    if os.path.exists(file_name):\n        with open(file_name, \'rb\') as f:\n            return compress_pickle.load(f, compression="lzma")\n            # return pickle.load(f)\n    else:\n        return None\n\n\n\n"""\ngit add . && git commit -m "Options" && git push &&  pip install git+ssh://git@gitlab.compute.dtu.dk/tuhe/unitgrade.git --upgrade\n\n"""\nimport unittest\nimport numpy as np\nimport os\nfrom io import StringIO\nimport sys\nimport collections\nimport inspect\n\nmyround = lambda x: np.round(x)  # required.\nmsum = lambda x: sum(x)\nmfloor = lambda x: np.floor(x)\n\ndef setup_dir_by_class(C,base_dir):\n    name = C.__class__.__name__\n    # base_dir = os.path.join(base_dir, name)\n    # if not os.path.isdir(base_dir):\n    #     os.makedirs(base_dir)\n    return base_dir, name\n\nclass Hidden:\n    def hide(self):\n        return True\n\nimport sys\n\nclass Logger(object):\n    def __init__(self, buffer):\n        self.terminal = sys.stdout\n        self.log = buffer\n\n    def write(self, message):\n        self.terminal.write(message)\n        self.log.write(message)\n\n    def flush(self):\n        # this flush method is needed for python 3 compatibility.\n        pass\n\n# sys.stdout = Logger()\n\nclass Capturing(list):\n    def __init__(self, *args, unmute=False, **kwargs):\n        self.unmute = unmute\n        super().__init__(*args, **kwargs)\n\n    def __enter__(self, capture_errors=True): # don\'t put arguments here.\n        self._stdout = sys.stdout\n        self._stringio = StringIO()\n        if self.unmute:\n            sys.stdout = Logger(self._stringio)\n        else:\n            sys.stdout = self._stringio\n\n        if capture_errors:\n            self._sterr = sys.stderr\n            sys.sterr = StringIO() # memory hole it\n        self.capture_errors = capture_errors\n        return self\n\n    def __exit__(self, *args):\n        self.extend(self._stringio.getvalue().splitlines())\n        del self._stringio    # free up some memory\n        sys.stdout = self._stdout\n        if self.capture_errors:\n            sys.sterr = self._sterr\n\n\nclass QItem(unittest.TestCase):\n    title = None\n    testfun = unittest.TestCase.assertEqual\n    tol = 0\n\n    def __init__(self, working_directory=None, correct_answer_payload=None, *args, **kwargs):\n        self.name = self.__class__.__name__\n        self._correct_answer_payload = correct_answer_payload\n        super().__init__(*args, **kwargs)\n        if self.title is None:\n            self.title = self.name\n\n    def assertL2(self, computed, expected, tol=None):\n        if tol == None:\n            tol = self.tol\n        diff = np.abs( (np.asarray(computed) - np.asarray(expected)) )\n        if np.max(diff) > tol:\n            print("Not equal within tolerance {tol}")\n            print(f"Element-wise differences {diff.tolist()}")\n            self.assertEqual(computed, expected, msg=f"Not equal within tolerance {tol}")\n\n    def assertL2Relative(self, computed, expected, tol=None):\n        if tol == None:\n            tol = self.tol\n        diff = np.abs( (np.asarray(computed) - np.asarray(expected)) )\n        diff = diff / (1e-8 + np.abs( (np.asarray(computed) + np.asarray(expected)) ) )\n        if np.sum(diff > tol) > 0:\n            print(f"Not equal within tolerance {tol}")\n            print(f"Element-wise differences {diff.tolist()}")\n            self.assertEqual(computed, expected, msg=f"Not equal within tolerance {tol}")\n\n    def compute_answer(self, unmute=False):\n        raise NotImplementedError("test code here")\n\n    def test(self, computed, expected):\n        self.testfun(computed, expected)\n\n    def get_points(self, verbose=False, show_expected=False, show_computed=False,unmute=False, passall=False, **kwargs):\n        possible = 1\n        computed = None\n        def show_computed_(computed):\n            print(">>> Your output:")\n            print(computed)\n\n        def show_expected_(expected):\n            print(">>> Expected output:")\n            print(expected)\n\n        try:\n            if unmute:\n                print("\\n")\n            computed = self.compute_answer(unmute=unmute)\n        except Exception as e:\n            if not passall:\n                print("\\n=================================================================================")\n                print(f"When trying to run test class \'{self.name}\' your code threw an error:")\n                print(e)\n                print("=================================================================================")\n                import traceback\n                traceback.print_exc()\n                return (0, possible)\n        correct = self._correct_answer_payload\n        if show_expected or show_computed:\n            print("\\n")\n        if show_expected:\n            show_expected_(correct)\n        if show_computed:\n            show_computed_(computed)\n        try:\n            # print(computed, correct)\n            # if passall:\n            #     computed = correct\n            if not passall:\n                self.test(computed=computed, expected=correct)\n        except Exception as e:\n            print("\\n=================================================================================")\n            print(f"Test output from test class \'{self.name}\' does not match expected result. Test error:")\n            print(e)\n            show_computed_(computed)\n            show_expected_(correct)\n            # print("-------------------------Your output:--------------------------------------------")\n            # print(computed)\n            # print("-------------------------Expected output:----------------------------------------")\n            # print(correct)\n            # print("=================================================================================")\n            return (0, possible)\n        return (1, possible)\n\n    def score(self):\n        try:\n            self.test()\n        except Exception as e:\n            return 0\n        return 1\n\nclass QPrintItem(QItem):\n    def compute_answer_print(self):\n        """\n        Generate output which is to be tested. By default, both text written to the terminal using print(...) as well as return values\n        are send to process_output (see compute_answer below). In other words, the text generated is:\n\n        res = compute_Answer_print()\n        txt = (any terminal output generated above)\n        numbers = (any numbers found in terminal-output txt)\n\n        self.test(process_output(res, txt, numbers), <expected result>)\n\n        :return: Optional values for comparison\n        """\n        raise Exception("Generate output here. The output is passed to self.process_output")\n\n    def process_output(self, res, txt, numbers):\n        return (res, txt)\n\n    def compute_answer(self, unmute=False):\n        with Capturing(unmute=unmute) as output:\n            res = self.compute_answer_print()\n        s = "\\n".join(output)\n        numbers = extract_numbers(s)\n        return self.process_output(res, s, numbers)\n\nclass OrderedClassMembers(type):\n    @classmethod\n    def __prepare__(self, name, bases):\n        return collections.OrderedDict()\n    def __new__(self, name, bases, classdict):\n        classdict[\'__ordered__\'] = [key for key in classdict.keys() if key not in (\'__module__\', \'__qualname__\')]\n        return type.__new__(self, name, bases, classdict)\n\nclass QuestionGroup(metaclass=OrderedClassMembers):\n    title = "Graph search"\n    items = None\n    partially_scored = False\n\n    def __init__(self, *args, **kwargs):\n        self.name = self.__class__.__name__\n        if self.items is None:\n            self.items = []\n            members = [gt for gt in [getattr(self, gt) for gt in self.__ordered__] if inspect.isclass(gt) and issubclass(gt, QItem)]\n            for gt in members:\n                self.items.append( (gt, 1) )\n        self.items = [(I(), w) for I, w in self.items]\n\nclass Report():\n    title = "report title"\n    questions = []\n    pack_imports = []\n\n    def __init__(self, strict=False,payload=None):\n        working_directory = os.path.abspath(os.path.dirname(inspect.getfile(type(self))))\n        # working_directory = os.path.join(pathlib.Path(__file__).parent.absolute(), "payloads/")\n        self.wdir, self.name = setup_dir_by_class(self, working_directory)\n        self.computed_answers_file = os.path.join(self.wdir, self.name + "_resources_do_not_hand_in.dat")\n        self.questions = [(Q(working_directory=self.wdir),w) for Q,w in self.questions]\n        # self.strict = strict\n        if payload is not None:\n            self.set_payload(payload, strict=strict)\n        else:\n            if os.path.isfile(self.computed_answers_file):\n                self.set_payload(cache_read(self.computed_answers_file), strict=strict)\n            else:\n                s = f"> Warning: The pre-computed answer file, {os.path.abspath(self.computed_answers_file)} is missing. The framework will NOT work as intended. Reasons may be a broken local installation."\n                if strict:\n                    raise Exception(s)\n                else:\n                    print(s)\n\n    def set_payload(self, payloads, strict=False):\n        for q, _ in self.questions:\n            for item, _ in q.items:\n                if q.name not in payloads or item.name not in payloads[q.name]:\n                    s = f"> Broken resource dictionary submitted to unitgrade for question {q.name} and subquestion {item.name}. Framework will not work."\n                    if strict:\n                        raise Exception(s)\n                    else:\n                        print(s)\n                item._correct_answer_payload = payloads[q.name][item.name][\'payload\']\n\ndef extract_numbers(txt):\n    import re\n    numeric_const_pattern = \'[-+]? (?: (?: \\d* \\. \\d+ ) | (?: \\d+ \\.? ) )(?: [Ee] [+-]? \\d+ ) ?\'\n    rx = re.compile(numeric_const_pattern, re.VERBOSE)\n    all = rx.findall(txt)\n    all = [float(a) if \'.\' in a else int(a) for a in all]\n    return all\n\n\nimport numpy as np\nfrom tabulate import tabulate\nfrom datetime import datetime\nimport pickle\nimport pyfiglet\n\n# from unitgrade.unitgrade import Hidden\n# import unitgrade as ug\n# import unitgrade.unitgrade as ug\nimport inspect\nimport os\nimport argparse\n\n\nparser = argparse.ArgumentParser(description=\'Evaluate your report.\', epilog="""Example: \nTo run all tests in a report: \n\n> python report1.py\n\nTo run only question 2 or question 2.1\n\n> python report1.py -q 2\n> python report1.py -q 2.1\n\nNote this scripts does not grade your report. To grade your report, use:\n\n> python report1_grade.py\n\nFinally, note that if your report is part of a module (package), and the report script requires part of that package, the -m option for python may be useful.\nAs an example, suppose the report file is Documents/course_package/report1.py, and `course_package` is a python package. Change directory to \'Documents/` and execute:\n\n> python -m course_package.report1\n\nsee https://docs.python.org/3.9/using/cmdline.html\n""", formatter_class=argparse.RawTextHelpFormatter)\nparser.add_argument(\'-q\', nargs=\'?\', type=str, default=None, help=\'Only evaluate this question (example: -q 2)\')\nparser.add_argument(\'--showexpected\',  action="store_true",  help=\'Show the expected/desired result\')\nparser.add_argument(\'--showcomputed\',  action="store_true",  help=\'Show the answer your code computes\')\nparser.add_argument(\'--unmute\',  action="store_true",  help=\'Show result of print(...) commands in code\')\nparser.add_argument(\'--passall\',  action="store_true",  help=\'Automatically pass all tests. Useful when debugging.\')\n\n# parser.add_argument(\'integers\', metavar=\'N\', type=int, nargs=\'+\',\n#                     help=\'an integer for the accumulator\')\n# parser.add_argument(\'--sum\', dest=\'accumulate\', action=\'store_const\',\n#                     const=sum, default=max,\n#                     help=\'sum the integers (default: find the max)\')\n\n\n\ndef evaluate_report_student(report, question=None, qitem=None):\n    args = parser.parse_args()\n    if question is None and args.q is not None:\n        question = args.q\n        if "." in question:\n            question, qitem = [int(v) for v in question.split(".")]\n        else:\n            question = int(question)\n\n    # print(args)\n    results, table_data = evaluate_report(report, question=question, qitem=qitem, verbose=False, passall=args.passall, show_expected=args.showexpected, show_computed=args.showcomputed,unmute=args.unmute)\n\n    if question is None:\n        print("Provisional evaluation")\n        tabulate(table_data)\n        table = table_data\n        print(tabulate(table))\n        print(" ")\n    print("Note your results have not yet been registered. \\nTo register your results, please run the file:")\n\n    fr = inspect.getouterframes(inspect.currentframe())[1].filename\n    print(">>>", os.path.basename(fr)[:-3] + "_grade.py")\n    print("In the same manner as you ran this file.")\n    return results\n\n\ndef upack(q):\n    # h = zip([(i[\'w\'], i[\'possible\'], i[\'obtained\']) for i in q.values()])\n    h =[(i[\'w\'], i[\'possible\'], i[\'obtained\']) for i in q.values()]\n    h = np.asarray(h)\n    return h[:,0], h[:,1], h[:,2],\n    #\n    # ws, possible, obtained = (np.asarray(x).squeeze() for x in zip([(i[\'w\'], i[\'possible\'], i[\'obtained\']) for i in q.values()]))\n    # return ws, possible, obtained\n\ndef evaluate_report(report, question=None, qitem=None, passall=False, verbose=False,  show_expected=False, show_computed=False,unmute=False):\n    now = datetime.now()\n    # show_expected = True\n    ascii_banner = pyfiglet.figlet_format("UnitGrade", font="doom")\n    b = "\\n".join( [l for l in ascii_banner.splitlines() if len(l.strip()) > 0] )\n    print(b + " v" + __version__)\n    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")\n    print("Started: " + dt_string)\n    print("Evaluating " + report.title, "(use --help for options)")\n    print(f"Loaded answers from: ", report.computed_answers_file, "\\n")\n    table_data = []\n    nL = 80\n\n    score = {}\n    for n, (q, w) in enumerate(report.questions):\n        q_hidden = issubclass(q.__class__, Hidden)\n        if question is not None and n+1 != question:\n            continue\n\n        print(f"Question {n+1}: {q.title}")\n        print("="*nL)\n        q.possible = 0\n        q.obtained = 0\n\n        q_ = {} # Gather score in this class.\n        for j, (item, iw) in enumerate(q.items):\n            if qitem is not None and question is not None and item is not None and j+1 != qitem:\n                continue\n\n            ss = f"*** q{n+1}.{j+1}) {item.title}"\n            el = nL-4\n            if len(ss) < el:\n                ss += \'.\'*(el-len(ss))\n            hidden = issubclass(item.__class__, Hidden)\n            if not hidden:\n                print(ss, end="")\n            (current, possible) = item.get_points(show_expected=show_expected, show_computed=show_computed,unmute=unmute, passall=passall)\n            q_[j] = {\'w\': iw, \'possible\': possible, \'obtained\': current, \'hidden\': hidden}\n            # q.possible += possible * iw\n            # q.obtained += current * iw\n            if not hidden:\n                if current == possible:\n                    print(f"PASS")\n                else:\n                    print(f"*** FAILED")\n\n        ws, possible, obtained = upack(q_)\n        possible = int(ws @ possible)\n        obtained = int(ws @ obtained)\n        obtained = int(myround(int((w * obtained) / possible ))) if possible > 0 else 0\n        score[n] = {\'w\': w, \'possible\': w, \'obtained\': obtained, \'Ã­tems\': q_, \'hidden\': q_hidden}\n\n        q.obtained = obtained\n        q.possible = possible\n\n        s1 = f"*** Question q{n+1}"\n        s2 = f" {q.obtained}/{w}"\n        print(s1 + ("."* (nL-len(s1)-len(s2) )) + s2 )\n        print(" ")\n        table_data.append([f"Question q{n+1}", f"{q.obtained}/{w}"])\n\n    ws, possible, obtained = upack(score)\n    possible = int( msum(possible) )\n    obtained = int( msum(obtained) ) # Cast to python int\n    report.possible = possible\n    report.obtained = obtained\n    now = datetime.now()\n    dt_string = now.strftime("%H:%M:%S")\n    print(f"Completed: "+ dt_string)\n    table_data.append(["Total", ""+str(report.obtained)+"/"+str(report.possible) ])\n    results = {\'total\': (obtained, possible), \'details\': score}\n    return results, table_data\n\n\nfrom tabulate import tabulate\nfrom datetime import datetime\nimport inspect\nimport json\nimport os\nimport bz2\nimport pickle\n\ndef bzwrite(json_str, token): # to get around obfuscation issues\n    with getattr(bz2, \'open\')(token, "wt") as f:\n        f.write(json_str)\n\ndef gather_upload_to_campusnet(report, output_dir=None):\n    n = 80\n    results, table_data = evaluate_report(report)\n    print(" ")\n    print("="*n)\n    print("Final evaluation")\n    print(tabulate(table_data))\n    # also load the source code of missing files...\n    results[\'sources\'] = {}\n    print("Gathering files...")\n    for m in report.pack_imports:\n        with open(m.__file__, \'r\') as f:\n            results[\'sources\'][m.__name__] = f.read()\n        print(f"*** {m.__name__}")\n\n    results[\'sources\'] = {}\n    json_str = json.dumps(results, indent=4)\n    # now = datetime.now()\n    # dname = os.path.dirname(inspect.getfile(report.__class__))\n    # dname = os.getcwd()\n    if output_dir is None:\n        output_dir = os.getcwd()\n\n    payload_out_base = report.__class__.__name__ + "_handin"\n\n    obtain, possible = results[\'total\']\n    token = "%s_%i_of_%i.token"%(payload_out_base, obtain, possible) # + str(obtained) +"_" +  ".token"\n    token = os.path.join(output_dir, token)\n    bzwrite(json_str, token)\n\n    print(" ")\n    print("To get credit for your results, please upload the single file: ")\n    print(">", token)\n    print("To campusnet without any modifications.")\n\ndef source_instantiate(name, report1_source, payload):\n    eval("exec")(report1_source, globals())\n    pl = pickle.loads(payload)\n    report = eval(name)(payload=pl, strict=True)\n    # report.set_payload(pl)\n    return report\n\n\nfrom cs101courseware_example import homework1\n\nclass ListReversalQuestion(QuestionGroup):\n    title = "Reversal of list"\n\n    class ListReversalItem(QPrintItem):\n        l = [1, 3, 5, 1, 610]\n        def compute_answer_print(self):\n            from cs101courseware_example.homework1 import reverse_list\n            return reverse_list(self.l)\n\n    class ListReversalWordsItem(ListReversalItem):\n        l = ["hello", "world", "summer", "dog"]\n\nclass LinearRegressionQuestion(QuestionGroup):\n    title = "Linear regression and Boston dataset"\n    class CoefficientsItem(QPrintItem):\n        testfun = QPrintItem.assertL2\n        tol = 0.03\n\n        def compute_answer_print(self):\n            from cs101courseware_example.homework1 import boston_linear\n            boston_linear()\n\n        def process_output(self, res, txt, numbers):\n            return numbers[:-1]\n\n    class RMSEItem(CoefficientsItem):\n        def process_output(self, res, txt, numbers):\n            return numbers[-1]\n\nclass Report1(Report):\n    title = "CS 101 Report 1"\n    questions = [(ListReversalQuestion, 5), (LinearRegressionQuestion, 13)]\n    pack_imports = [homework1] # Include this file in .token file'
WebLqOFrgMVsHPQuIXBU=b'\x80\x03}q\x00(X\x14\x00\x00\x00ListReversalQuestionq\x01}q\x02(X\x10\x00\x00\x00ListReversalItemq\x03}q\x04X\x07\x00\x00\x00payloadq\x05]q\x06(Mb\x02K\x01K\x05K\x03K\x01eX\x00\x00\x00\x00q\x07\x86q\x08sX\x15\x00\x00\x00ListReversalWordsItemq\t}q\nh\x05]q\x0b(X\x03\x00\x00\x00dogq\x0cX\x06\x00\x00\x00summerq\rX\x05\x00\x00\x00worldq\x0eX\x05\x00\x00\x00helloq\x0feh\x07\x86q\x10suX\x18\x00\x00\x00LinearRegressionQuestionq\x11}q\x12(X\x10\x00\x00\x00CoefficientsItemq\x13}q\x14h\x05]q\x15(G\xbf\xbb\xa8"\x03\xc7\x1b\x18G?\xa7\xc4Gy-\x96\xd1G?\x94\xea\xdd\x08M9@G@\x05\x81\x15 \xce\x81\xaeG\xc01\xc3\xc7[s\xc4\x1dG@\x0e}g\x88zbrG?GB;\xd8\r\xa6KG\xbf\xf7\x9a\xf1\x0c\xf3\x02\x97G?\xd3\x95\xfa\x13h"\xe5G\xbf\x89D\x06\xeep[iG\xbf\xee{\t\x0e\x82\xb5\xe4G?\x83\x13Zm\xbcH\x7fG\xbf\xe0\xc9*\xc7\xba\xfbOesX\x08\x00\x00\x00RMSEItemq\x16}q\x17h\x05G@\x12\xb7\x8a\xa8\xe06\xe6suu.'
WebLqOFrgMVsHPQuIXBi="Report1"
WebLqOFrgMVsHPQuIXBG=WebLqOFrgMVsHPQuIXjY(WebLqOFrgMVsHPQuIXBi,WebLqOFrgMVsHPQuIXBR,WebLqOFrgMVsHPQuIXBU)
WebLqOFrgMVsHPQuIXBf=WebLqOFrgMVsHPQuIXjC.dirname(__file__)
WebLqOFrgMVsHPQuIXjB(WebLqOFrgMVsHPQuIXBG,WebLqOFrgMVsHPQuIXBf)