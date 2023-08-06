# Unitgrade

Easy-to-use, easy-to-build report evaluations in a framework building on pythons unittest classes

- 100% Python
- No configuration or test-files needed to use or develop
- Easy to use for students: 
    - Run tests as a single python command 
    - See your score immediately 
    - Upload your results as a single file on campusnet with no risk of accidential tampering
- All tests are simple classes so it will integrates well with debugger and any IDE 

## Installation
Unitgrade can be installed through pip using 
```
pip install git+ssh://git@gitlab.compute.dtu.dk/tuhe/unitgrade.git
```
This will install unitgrade in your site-packages directory. If you want to upgrade an old installation of unitgrade:
```
pip install git+ssh://git@gitlab.compute.dtu.dk/tuhe/unitgrade.git --upgrade
```
If you are using anaconda+virtual environment you can install it as
```
source activate myenv
conda install git pip
pip install git+ssh://git@gitlab.compute.dtu.dk/tuhe/unitgrade.git
```
Alternatively, simply use git-clone of the sources and add unitgrade to your python path.

When you are done, you should be able to import unitgrade:
```
import unitgrade
```
## Testing installation
I have provided an example project which illustrates all main features in a self-contained manner and which should 
work immediately upon installation. The source can be found here: https://lab.compute.dtu.dk/tuhe/unitgrade/-/tree/master/cs101courseware_example
To run the example, first start a python console:
```
python
```
Then run the code
```
from cs101courseware_example import instructions
```
This will print on-screen instructions for how to use the system tailored to your user-specific installation path.

## Evaluating a report
Homework is broken down into **reports**. A report is a collection of questions which are individually scored, and each question may in turn involve multiple tests. Each report is therefore given an overall score based on a weighted average of how many tests are passed.
In practice, a report consist of an ordinary python file which they simply run. It looks like this (to run this on your local machine, follow the instructions in the previous section):
```
python cs101report1.py
```
The file `cs101report1.py` is just an ordinary, non-obfuscated file which they can navigate and debug using a debugger. The file may contain the homework, or it may call functions the students have written.  Running the file creates console output which tells the students their current score for each test:

```
Starting on 02/12/2020 14:57:06
Evaluating CS 101 Report 1

Question 1: Reversal of list
================================================================================
*** q1.1) ListReversalItem..................................................PASS
*** q1.2) ListReversalWordsItem.............................................PASS
*** Question q1............................................................. 5/5

Question 2: Linear regression and Boston dataset
================================================================================
*** q2.1) CoefficientsItem..................................................PASS
*** q2.2) RMSEItem..........................................................PASS
*** Question q2........................................................... 13/13

Finished at 14:57:06
Provisional evaluation
-----------  -----
Question q1  5/5
Question q2  13/13
Total        18/18
-----------  -----

Note your results have not yet been registered.
To register your results, please run the file:
>>> cs101report1_grade.py
In the same manner as you ran this file.
```
Once you are happy with the result, run the alternative, not-easy-to-tamper-with script called `cs101report1_grade.py`:

```
python cs101report1_grade.py
```
This runs the same tests, and generates a file `Report0_handin_18_of_18.token`. The file name indicates how many points you got. Upload this file to campusnet.

### Why are there two scripts?
The reason why we use a standard test script, and one with the `_grade.py` extension, is because the tests should both be easy to debug, but at the same time we have to prevent accidential changes to the test scripts. Hence, we include two versions of the tests.

## FAQ
 - **My non-grade script and the `_grade.py` script gives different number of points**
Since the two scripts should contain the same code, the reason is nearly certainly that you have made an (accidental) change to the test scripts. Please ensure both scripts are up-to-date and if the problem persists, try to get support.
   
 - **Why is there a `*_resources_do_not_hand_in.dat` file? Should I also upload it?**
No. The file contains the pre-computed test results your code is compared against. If you want to load this file manually, the unitgrade package contains helpful functions for doing so.
   
 - **I am worried you might think I cheated because I opened the '_grade.py' script/token file**
This should not be a concern. Both files are in a binary format (i.e., if you open them in a text editor they look like garbage), which means that if you make an accidential change, they will with all probability simply fail to work. 
   
 - **I think I might have edited the `report1.py` file. Is this a problem since one of the tests have now been altered?**
Feel free to edit/break this file as much as you like if it helps you work out the correct solution. In fact, I recommend you just run `report1.py` from your IDE and use the debugger to work out the current state of your program. However, since the `report1_grade.py` script contains a seperate version of the tests, please ensure your `report1.py` file is up to date.
   
### Debugging your code/making the tests pass
The course material should contain information about the intended function of the scripts used in the tests, and the file `report1.py` should mainly be used to check which of your code is being run. In other words, first make sure your code solves the exercises, and only later run the test script which is less easy/nice to read. 
However, obivously you might get to a situation where your code seems to work, but a test fails. In that case, it is worth looking into the code in `report1.py` to work out what is going on. 

 - **I am 99% sure my code is correct, but the test still fails. Why is that?**
The testing framework offers a great deal of flexibility in terms of what is compared. This is either: (i) The value a function returns, (ii) what the code print to the console (iii) something derived from these.
   Since the test *might* compare the console output, i.e. what you generate using `print("...")`-statements, innnocent changes to the script, like an extra print statement, can cause the test to fail, which is counter-intuitive. For this reason, please look at the error message carefully (or the code in `report1.py`) to understand what is being compared. 
   
One possibility that might trick some is that if the test compares a value computed by your code, the datatype of that value is important. For instance, a `list` is not the same as a python `ndarray`, and a `tuple` is different from a `list`. This is the correct behavior of a test: These things are not alike and correct code should not confuse them. 

 - **The `report1.py` class is really confusing. I can see the code it runs on my computer, but not the expected output. Why is it like this?**
To make sure the desired output of the tests is always up to date, the tests are computed from a working version of the code and loaded from the disk rather than being hard-coded.

 - **How do I see the output of my programs in the tests? Or the intended output?**
There are a number of console options available to help you figure out what your program should output and what it currently outputs. They can be found using:
 ```python report1.py --help```
Note these are disabled for the `report1_grade.py` script to avoid confusion. It is not recommended you use the grade script to debug your code.  

 - **How do I see the output generated by my scripts in the IDE?**
The file `unitgrade/unitgrade.py` contains all relevant information. Look at the `QItem` class and the function `get_points`, which is the function that strings together all the tests. 

 - **Since I cannot read the `.token` file, can I trust it contains the same number of points internally as the file name indicate?**
Yes. 

### Privacy/security   
 - **I managed to reverse engineer the `report1_grade.py`/`*.token` files in about 30 minutes. If the safety measures are so easily broken, how do you ensure people do not cheat?**
That the script `report1_grade.py` is difficult to read is not the principle safety measure. Instead, it ensures there is no accidential tampering. If you muck around with these files and upload the result, we will very likely know.     

- **I have private data on my computer. Will this be read or uploaded?**
No. The code will look for and upload your solutions, but it will not read/look at other directories in your computer. In the example provided with this code, this means you should expect unitgrade to read/run all files in the `cs101courseware_example`-directory, but **no** other files on your computer (unless some code in this directory load other files). So as long as you keep your private files out of the base courseware directory, you should be fine. 

- **Does this code install any spyware/etc.? Does it communicate with a website/online service?**
No. Unitgrade makes no changes outside the courseware directory and it does not do anything tricky. It reads/runs code and write the `.token` file.
  
- **I still have concerns about running code on my computer I cannot easily read**
Please contact me and we can discuss your specific concerns.
  
