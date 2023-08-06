from unitgrade.unitgrade import QuestionGroup, Report, QPrintItem
from unitgrade.unitgrade_helpers import evaluate_report_student
from cs101courseware_example import homework1

class ListReversalQuestion(QuestionGroup):
    title = "Reversal of list"

    class ListReversalItem(QPrintItem):
        l = [1, 3, 5, 1, 610]
        def compute_answer_print(self):
            from cs101courseware_example.homework1 import reverse_list
            return reverse_list(self.l)

    class ListReversalWordsItem(ListReversalItem):
        l = ["hello", "world", "summer", "dog"]

class LinearRegressionQuestion(QuestionGroup):
    title = "Linear regression and Boston dataset"
    class CoefficientsItem(QPrintItem):
        testfun = QPrintItem.assertL2
        tol = 0.03

        def compute_answer_print(self):
            from cs101courseware_example.homework1 import boston_linear
            boston_linear()

        def process_output(self, res, txt, numbers):
            return numbers[:-1]

    class RMSEItem(CoefficientsItem):
        def process_output(self, res, txt, numbers):
            return numbers[-1]

class Report1(Report):
    title = "CS 101 Report 1"
    questions = [(ListReversalQuestion, 5), (LinearRegressionQuestion, 13)]
    pack_imports = [homework1] # Include this file in .token file

if __name__ == "__main__":
    evaluate_report_student(Report1())
