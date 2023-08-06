from sklearn.linear_model import LinearRegression

class linregressor:


    """

    The linregressor class offers certain functions useful for linear regression modelling. These are as follows:

    1. linregTrain()
    2. prediction()
    3. test()

    """

    def __init__(self):
        self.__linreg = LinearRegression()

    def linregTrain(self, xtrain, ytrain):
        """

        :param xtrain:
        :param ytrain:
        :return train, coeff, intercept:

        It takes the xtrain, ytrain, fits it and returns the training object, coeffficient value and the intercept values.

        """
        train =  self.__linreg.fit(xtrain, ytrain)
        coeff = self.__linreg.coef_
        intercept = self.__linreg.intercept_
        return train, coeff, intercept

    def prediction(self, x):
        """
        :param x:
        :return linreg.predict(x):

        It takes the input values for the prediction and returns the predicted result.

        """
        return self.__linreg.predict(x)

    def __adjR2Score(self,x,y):
        r2 = self.__linreg.score(x,y)
        n = x.shape[0]
        p = x.shape[1]
        adjusted_r2 = 1-(1-r2)*(n-1)/(n-p-1)
        return adjusted_r2

    def test(self, xtest, ytest, score_type = ['r2_score']):
        """
        :param xtest:
        :param ytest:
        :param score_type:
        :return score:

        It takes input the xtest, ytest values and score_types list and returns the score list

        Accpeted score_types are : 'r2_score', 'adj_r2_score'

        """
        score = []
        for i in score_type:
            if i.lower() == 'r2_score':
                score.append(self.__linreg.score(xtest, ytest))
            elif i.lower() == 'adj_r2_score':
                score.append(self.__adjR2Score(xtest,ytest))
        return score

