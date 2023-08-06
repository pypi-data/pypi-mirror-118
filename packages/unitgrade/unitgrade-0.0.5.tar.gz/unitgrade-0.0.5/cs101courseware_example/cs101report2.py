from unitgrade.unitgrade import QuestionGroup, Report, QPrintItem, Hidden

class ListReversalQuestion(QuestionGroup):
    title = "Reversal of list"
    class ListReversalItem(QPrintItem):
        l = [1, 3, 5, 1, 610]
        def compute_answer_print(self):
            from cs101courseware.homework1 import reverse_list
            print(reverse_list(self.l))

    class ListReversalWordsItem(ListReversalItem):
        l = ["hello", "world", "summer", "dog"]

    class ListReversalWordsItemHidden(ListReversalItem, Hidden):
        l = ["hello", "world", "summer", "dog"]

# class LinearRegressionQuestion(QuestionGroup):
#     title = "Linear regression and Boston dataset"
#     class CoefficientsItem(QPrintItem):
#         testfun = QPrintItem.assertL2
#         tol = 0.03
#
#         def compute_answer_print(self):
#             from cs101courseware_example.homework1 import boston_linear
#             boston_linear()
#
#         def process_output(self, res, txt, numbers):
#             return numbers[:-1]
#
#     class RMSEItem(CoefficientsItem):
#         def process_output(self, res, txt, numbers):
#             return numbers[-1]

class Report2(Report):
    title = "CS 101 Report 2"
    questions = [(ListReversalQuestion, 5), ]
    pack_imports = [] # Include this file in .token file

if __name__ == "__main__":
    # from unitgrade_private.hidden_create_files import setup_answers, setup_grade_file_report
    from unitgrade.unitgrade_helpers import evaluate_report_student
    # setup_grade_file_report(Report2, minify=True, bzip=True, obfuscate=True)
    # evaluate_report_student(Report2())
    evaluate_report_student(Report2())


