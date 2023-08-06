import pandas as pd
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

def getInfo(data):
    '''
    Method Name:getInfo
    Description: This method calls the DataFrame's info() method

    Parameters
    ----------
    data : Can be a dataframe, list, or a series

    Returns
    -------
    dataframe : A dataframe with all the columns, their total observations and data type

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    preprocessor.getInfo(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''

    try:
        if isinstance(data, (list, pd.core.series.Series)):
            df = pd.DataFrame(data)
            return df.info()
        elif isinstance(data, pd.core.frame.DataFrame):
            return data.info()
        else:
            return 'Please pass DataFrame, Series or List in the argument'

    except Exception as e:
        return Exception(e)

def getDescribe(data):
    '''
    Method Name:getDescribe
    Description: This method calls the DataFrame's describe() method

    Parameters
    ----------
    data : Can be a dataframe, list, or a series

    Returns
    -------
    dataframe : A dataframe with all statistical information about data distribution

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    preprocessor.getDescribe(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(data, (list, pd.core.series.Series)):
            df = pd.DataFrame(data)
            return df.describe().T
        elif isinstance(data, pd.core.frame.DataFrame):
            return data.describe().T
        else:
            return 'Please pass DataFrame, Series or List in the argument'
    except Exception as e:
        return Exception(e)



def getHead(df, num):
    '''
    Method Name:getHead
    Description: This method calls the DataFrame's head() method

    Parameters
    ----------
    df  : a dataframe,
    num : number of observations to be viewed

    Returns
    -------
    dataframe : Return first 'num' number of observations for the dataframe

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    preprocessor.getHead(df,5)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            return df.head(num)
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def getHeadforFirstFive(df):
    '''
    Method Name:getHeadforFirstFive
    Description: This method calls the DataFrame's head() method

    Parameters
    ----------
    df  : a dataframe

    Returns
    -------
    dataframe : Return first 5 number of observations for the dataframe

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    preprocessor.getHeadforFirstFive(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            return df.head()
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def loadcsv(file):
    '''
    Method Name:loadcsv
    Description: This method calls the DataFrame's read_csv() method

    Parameters
    ----------
    file  : path to the csv file

    Returns
    -------
    dataframe : Return a dataframe

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        return pd.read_csv(file)
    except Exception as e:
        return Exception(e)

def getTailForLastFive(df):
    '''
    Method Name:getTailForLastFive
    Description: This method calls the DataFrame's tail() method

    Parameters
    ----------
    df  : a dataframe

    Returns
    -------
    dataframe : Return last 5 number of observations of the dataframe

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    preprocessor.getTailForLastFive(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            return df.tail()
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def getTail(df, num):
    '''
    Method Name:getTail
    Description: This method calls the DataFrame's tail() method

    Parameters
    ----------
    df  : a dataframe
    num : number of observations to display

    Returns
    -------
    dataframe : Return last num number of observations of the dataframe

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    preprocessor.getTail(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            return df.tail(num)
        else:
            return 'Pass a valid dataFrame'
    except Exception as e:
        return Exception(e)

def checkNull(df):
    '''
    Method Name:checkNull
    Description: This method calls the dataframe's isnull().sum() method

    Parameters
    ----------
    df  : a dataframe

    Returns
    -------
    dataframe : Returns a series with all of the columns from the dataframe and the sum of their null values

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    preprocessor.checkNull(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            return df.isnull().sum()
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def dropVariables(df,varlist,axis,inplace):
    '''
    Method Name:dropColumns
    Description: This method calls the dataframe's drop method

    Parameters
    ----------
    df      : a dataframe,
    varlist : list of columns to drop,
    axis    : Either 0 -> rows, 1 ->columns
    inplace : Either True, False

    Returns
    -------
    Depending on inplace, if set 'True' will remove the columns from the original dataframe which is passed in the argument

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')

    For multiple varlist
    =====================
    preprocessor.dropVariables(df,['Age','Weight'],1,True)

    For single entry in the varlist
    ================================
    preprocessor.dropVariables(df,['Age'],1,True)


    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            if len(varlist) != 0 and axis >= 0 and inplace >= 0:
                df.drop(varlist, axis=axis, inplace=inplace)
            else:
                return 'Pass valid arguments'
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def createdummies(df):
    '''
    Method Name:createdummies
    Description: This method calls the dataframe's get_dummies() method to create dummies for categorical variables

    Parameters
    ----------
    df  : a dataframe

    Returns
    -------
    dataframe : Returns the original dataframe with the dummies incorporated

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    df = preprocessor.createdummies(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            cat_features = [i for i in df.columns if df[i].dtypes == 'object']
            for feature in cat_features:
                if len(df[feature].unique()) > 1:
                    col_dummies = pd.get_dummies(df[feature], prefix=feature, drop_first=True)
                    df = pd.concat([df,col_dummies], axis = 1)
                    df.drop(feature, axis=1, inplace= True)
                    return df
                else:
                    df[feature] = df[feature].map(lambda x: 1)
                    return df
        else:
            return 'Pass a valid dataframe'

    except Exception as e:
        return Exception(e)

def findHighCorr_Vars(df,threshold):
    '''
    Method Name:findHighCorr_Vars
    Description: This method calls the dataframe's corr() method to get the correlation and then based on the threshold value, create a list of all the variables with high correlation
                 This method should be used to find correlation between independant variables (NOT TARGET Variable)
                 Use "separate_label_features" from this package to separate dependant and independant variables

    Parameters
    ----------
    df        : a dataframe,
    threshold : a threshold value(cut-off) which decides upto what value correlation is accepted between independant variables

    Returns
    -------
    dataframe : Returns a list of highly correlated variables

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    X,Y = preprocessor.separate_label_features(df,'Target Variable')
    arr = preprocessor.findHighCorr_Vars(X,7)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            corr_set = set()
            corr_matrix = df.corr()
            for i in range(len(corr_matrix.columns)):
                for j in range(i):
                    if corr_matrix.iloc[i,j] > threshold:
                        colName = corr_matrix.columns[i]
                        corr_set.add(colName)
            return list(corr_set)
        else:
            return 'Pass a valid dataframe'

    except Exception as e:
        return Exception(e)

def impute_missing_values(df,discrete=None):
    '''
    Method Name:impute_missing_values
    Description: This method calls the dataframe's fillna() method to fill the missing values with column's median,mode value depending on numerical or categorical data

    Parameters
    ----------
    df        : a dataframe,
    discrete  : Default value is None. Can take two values True or False. If discrete is set to True then we will handle discrete variables.

    Logic implemented to determine discrete variables from the numerical dataset
    -----------------------------------------------------------------------------
    The criteria is the variable should have more than 0 unique values and less than 5. if more than 5 then we will consider it as continuous variable. Median value will be considered if continuous or else mode value

    Returns
    -------
    dataframe : Returns the original dataframe with the missing values removed

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    df = preprocessor.impute_missing_values(df,True)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            for col in df.columns:
                if df[col].dtypes == 'object':
                    df[col] = df[col].fillna(df[col].mode())
                elif discrete:
                    discreteCol = pd.Categorical(df[col])
                    if len(discreteCol.categories) > 5:
                        df[col] = df[col].fillna(df[col].median())
                    else:
                        df[col] = df[col].fillna(df[col].mode())
                else:
                    df[col] = df[col].fillna(df[col].median())

            return df
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def impute_outliers(df,cols,type):
    '''
    Method Name:impute_outliers
    Description: This method calls the dataframe's quantile method to calculate Inter Quantile Range of the variable, based on which the upper and lower bounds for the variables are calculated

    Parameters
    ----------
    df   : a dataframe,
    cols : list of columns having outliers. You can find by plotting boxplot for each variables
    type : Can be three values "Gaussian, "Skewed", "Highly Skewed" depending on the distribution of the variable

    Expected Criteria
    -----------------
    The length of "types" list should be same as the length of "cols" list. Each column will have its disribution's name mentioned in the type list

    Logic implemented
    ------------------
    For Gaussian Distribution:
        bound  = df[variable].mean() +- 3 * df[variable].std()
    For Skewed Distribution:
        bound = df[variable].quantile(0.25) +- 1.5 * IQR
    For Highly Skewed Distribution:
        bound = df[variable].quantile(0.25) +- 3.0 * IQR

    Returns
    -------
    dataframe : Returns a dataframe with outliers handled

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    df = preprocessor.impute_outliers(df, ['Age','Salary', 'Fare'],['Gaussian','Skewed','Highly Skewed'])

    df = preprocessor.impute_outliers(df, ['Age','Salary', 'Fare'],['Gaussian','Gaussian','Highly Skewed'])


    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            if len(cols) == len(type):
                count = 0
                for variable in cols:
                    typestr = type[count]
                    if typestr == "Gaussian":
                        upper_bound = df[variable].mean() + 3 * df[variable].std()
                        lower_bound = df[variable].mean() - 3 * df[variable].std()
                        df[variable].clip(lower=lower_bound, inplace=True)
                        df[variable].clip(upper=upper_bound, inplace=True)
                    elif typestr == "Skewed":
                        IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)
                        lower_bound = df[variable].quantile(0.25) - 1.5 * IQR
                        upper_bound = df[variable].quantile(0.75) + 1.5 * IQR
                        df[variable].clip(lower=lower_bound, inplace=True)
                        df[variable].clip(upper=upper_bound, inplace=True)
                    else:
                        IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)
                        lower_bound = df[variable].quantile(0.25) - 3 * IQR
                        upper_bound = df[variable].quantile(0.75) + 3 * IQR
                        df[variable].clip(lower=lower_bound, inplace=True)
                        df[variable].clip(upper=upper_bound, inplace=True)

                    count = count + 1
                return df
            else:
                return 'Length of type and cols mismatch'
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def separate_label_features(df,labelName):
    '''
    Method Name:separate_label_features
    Description: This method separates the independant and dependant variables in the dataset

    Parameters
    ----------
    df        : a dataframe,
    labelName : name of the target variable

    Returns
    -------
    X,Y : X -> Independant Variables, Y -> Dependant Variable

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    X,Y = preprocessor.separate_label_features(df,'Target')



    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            X = df.drop(labelName, axis=1)
            Y = df[labelName]
            return X, Y
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def getScalarDistribution(df):
    '''
    Method Name:getScalarDistribution
    Description: This method calls the sklearn.preprocessing StandardScaler() to get the scaled distribution

    Parameters
    ----------
    df        : a dataframe

    Returns
    -------
    Array -> Returns an array of  scaled transformed

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    arr = preprocessor.getScalarDistribution(df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        if isinstance(df, pd.core.frame.DataFrame):
            scaler = StandardScaler()
            arr = scaler.fit_transform(df)
            return arr
        else:
            return 'Pass a valid dataframe'
    except Exception as e:
        return Exception(e)

def find_variance_inflation_factor(arr, df):
    '''
    Method Name:find_variance_inflation_factor
    Description: This method calls the statsmodels.stats.outlier_influence 's  variance_inflation_factor to calculate the VIF

    Parameters
    ----------
    arr : scaled transformed array. Find the scaled transformed array using
            df = preprocessor.loadcsv('FilePath')
            arr = preprocessor.getScalarDistribution(df)

    df  : a dataframe

    Returns
    -------
    List -> Returns list of variables with Variance Inflation Factor(VIF) greater than 10

    Examples
    --------
    df = preprocessor.loadcsv('FilePath')
    arr = preprocessor.getScalarDistribution(df)
    arr1 = preprocessor.find_variance_inflation_factor(arr,df)

    On Failure: Raise Exception
    Written By: Anupam Hore
    Version: 1.0
    Revisions: None
    '''
    try:
        vif = pd.DataFrame()
        vif['VIF'] = [variance_inflation_factor(arr, i) for i in range(arr.shape[1])]
        vif['Feature'] = df.columns
        series = vif[vif['VIF'] > 10]
        arr = list(series.Feature)
        return arr
    except Exception as e:
        return Exception(e)

