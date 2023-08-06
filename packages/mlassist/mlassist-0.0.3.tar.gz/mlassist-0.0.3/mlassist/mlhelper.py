import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from pandas_profiling import ProfileReport
from sklearn.preprocessing import MinMaxScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor


class mlhelp:


    """
    The mlhelp class offers certain helping functions for developing machine learning models. Following are the functions offered:

    1. readFile()
    2. printReport()
    3. describe()
    4. column_drop
    5. imputationNa()
    6. scale()
    7. vifCalc()
    8. trainTestSplitter()
    9. xysplit()


    """

    def __init__(self):
        pass

    def readFile(self,file_loc):
        """
        :param file_loc:
        :return data frame:

        It reads the file from file_loc and returns a pandas dataframe.

        Accepted file formats are:
        1. csv
        2. xls
        3. xlsx
        4. xlsm
        5. odf
        6. ods
        7. odt
        8. json

        """
        _,_,tail = file_loc.partition('.')
        if tail == 'csv':
            df = pandas.read_csv(file_loc)
        elif tail == 'xls' or tail == 'xlsx' or tail == 'xlsm' or tail == 'odf' or tail == 'ods' or tail == 'odt':
            df = pandas.read_excel(file_loc)
        elif tail == 'json':
            df = pandas.read_json(file_loc)
        return df

    def printReport(self, df):
        """

        :param df:
        :return ProfileReport(df):

        It reads the dataframe and returns a Pandas Profile Report of the dataframe.

        """
        pf = ProfileReport(df)
        return pf.to_widgets()

    def describe(self, df):

        """

        :param df:
        :return df.describe():

        It reads the dataframe and returns df.describe().

        """

        return df.describe()

    def column_drop(self, df, column_name):
        """

        :param df:
        :param column_name:
        :return dataframe after droping the column:

        It reads the dataframe and the column names to be dropped, drops those columns and returns the dataframe

        """
        return df.drop(columns = column_name)

    def imputationNa(self, df, imputation_dic):

        """

        :param df:
        :param imputation_dic:
        :return dataframe after imputing it.:

        It reads the dataframe, a dictionary "imputation_dic" of the following format:

        imputation_dic = {'mean': ['column1'...'column n'],
                        'median': ['column1'...'column n'],
                        'mode': ['column1'...'column n']}

        Acceptable keys for imputation_dic: 'mean', 'median', 'mode'

        It imputes the nan values in the given columns with the respective key values and returns the dataframe after imputing.

        """

        lst = imputation_dic.keys()
        for i in lst:
            if i.lower() == 'mean':
                for j in imputation_dic[i]:
                    df[j] = df[j].fillna(df[j].mean())
            elif i.lower() == 'median':
                for j in imputation_dic[i]:
                    df[j] = df[j].fillna(df[j].median())
            elif i.lower() == 'mode':
                for j in imputation_dic[j]:
                    df[j] = df[j].fillna(df[j].mode())
        return df

    def scale(self, df, scale_type, column_names = 0, all_columns = False):

        """
        :param df:
        :param scale_type:
        :param column_names (optional if all_columns = False):
        :param all_columns:
        :return dataframe after scaling:

        It reads a dataframe df, string scale_type, list column_names, boolean all_columns

        accepted values for scale_type = 'min_max', 'standard'
        column names consists of list of all the columns on which we need to apply scaling
        all_columns is a boolean value which is either True or False. If True, then all columns of the dataframe will be scaled.
        """
        if scale_type.lower() == 'min_max':
            scaler = MinMaxScaler()
            if all_columns == True:
                 arr =  scaler.fit_transform(df)
                 df = pandas.DataFrame(arr,columns=df.columns)
            else:
                for i in column_names:
                    df[i] = scaler.fit_transform(i)
        elif scale_type.lower() == 'standard':
            scaler = StandardScaler()
            if all_columns == True:
                arr = scaler.fit_transform(df)
                df = pandas.DataFrame(arr,columns=df.columns)
            else:
                for i in column_names:
                    df[i] = scaler.fit_transform(df)
        return df

    def vifCalc(self, df):
        """

        :param df:
        :return vif_df:

        This function reads the dataframe df and calculates the vif value for every column in the dataframe. After that it creates a dataframe
        vif_df with two columns 'vif' and 'feature' and returns it.
        """

        arr = df.to_numpy()
        vif_df = pandas.DataFrame()
        vif_df['vif'] = [variance_inflation_factor(arr, i) for i in range(arr.shape[1])]
        vif_df['feature'] = df.columns
        return vif_df

    def trainTestSplitter(self, x, y, test_size, random_state = None):

        """
        :param x:
        :param y:
        :param test_size:
        :param random_state:
        :return xtrain, xtest, ytrain, ytest:

        It reads the x value, y value, test_size, random_state

        x : independent varaibles
        y : dependent variable
        test_size : percentage of test data
        random_state : seed value

        And splits the data into train-test based on the test_size and random split then returns the xtrain, xtest, ytrain, ytest

        """
        if random_state == None:
            xtrain, xtest, ytrain, ytest = train_test_split(x,y,test_size = test_size)
        elif random_state != None:
            xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size = test_size, random_state = random_state)
        return xtrain, xtest, ytrain, ytest

    def xysplit(self, df, y):

        """


        :param df:
        :param y:
        :return x1,y1:

        It reads the dataframe df, the dependent variable y and splits it to independent dataframe x1 and dependent dataframe y1

        """
        y1 = df[y]
        x1 = df.drop(columns=[y])
        return x1,y1
