import numpy as np
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

####################
# Question 1. Write a function reverse_list which accepts a list, and returns a new list
# with the same elements but in opposite order.
####################
def reverse_list(mylist):
    # TODO: Your solution here
    result = []
    for k in mylist:
        result = [k] + result

    return result

def simple_list_question():
    print("The reverse list function can reverse a list")
    l = [1, 2, 3, 4]
    print("List was:", l, "reversed version", reverse_list(l))


####################
# Question 2: Write a function which performs linear regression on the Boston housing dataset using scipy
####################
def boston_linear():
    X,y = load_boston(return_X_y=True) # Load the dataset here
    y += np.random.randn(y.size ) * 0.01
    # TODO: Fit a linear regression model and print the coefficients
    lin_model = LinearRegression()
    lin_model.fit(X, y)
    print("Coefficients are", lin_model.coef_)
    # TODO: Compute the RMSE here (on the training set) and print it
    y_predict = lin_model.predict(X)
    rmse = (np.sqrt(mean_squared_error(y, y_predict)))
    print("RMSE is", rmse)

if __name__ == "__main__":
    simple_list_question()
    boston_linear()
