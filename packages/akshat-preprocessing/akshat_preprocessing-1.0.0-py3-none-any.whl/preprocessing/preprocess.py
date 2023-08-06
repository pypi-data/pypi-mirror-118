import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class Preprocessing:
    def __init__(self, file_name):
        """
        Author: Akshat Pant
        This is the __init__ function and it stores the filename
        passed by the user
        :param file_name: name of the csv file on which Preprocessing needs to be done
        """
        # self.dataframe = dataframe
        self.file_name = file_name

    def read_csv_file(self):
        """
        Author: Akshat Pant
        This function is used to read the csv file
        :return: dataframe containing all the records
        """
        try:
            self.df = pd.read_csv(self.file_name)
            return self.df
        except Exception as e:
            return "Error in Reading csv!! Please check!! Exception is: {}".format(e)


    def remove_column_by_name(self, df , *col_name):
        """
        Author: Akshat Pant
        This function is used to remove the columns from a dataframe
        :param df: name of dataframe whose columns need to be removed
        :param  col_name: name of columns to be removed, any number of column names can be passed
                and the col_name must be passed as comma-seprated string. For ex: if A,B,C,D needs to be removed then
                col_name must be "A,B,C,D"
        :return: new dataframe with removed columns
        """
        # pd.read_csv(self.dataframe).drop()
        try:
            col_list = []
            for col in col_name:
                col_list.append(col)
            # df_new = self.read_csv_file()
            df.drop(col_list, axis=1, inplace=True)
            return df
        except Exception as e:
            return "Error in removing columns!! Please check!! Exception is : {}".format(e)

    def find_missing_values(self, df):
        """
        Author: Akshat Pant
        This function is used to find the number of missing values in each column of the datframe
        :param df: name of dataframe of which missing values need to be find out
        :return: a dictionary containing 'key' as 'column name' and 'value' as the 'number of missing values'
        """
        try:
            return df.isnull().sum().to_dict()
        except Exception as e:
            return "Error in finding missing values!! Please Check!! Exception is : {}".format(e)

    def fill_missing_val_by_mean(self, df, *col_name):
        """
        Author: Akshat Pant
        This function is used to fill the missing value in the datframe with mean imputation
        :param df: name of dataframe whose missing value needs to be filled by mean value of the column
        :param  col_name: col_name: name of columns whose missing values need to be filled, any number
                of column names can be passed and the col_name must be passed as comma-seprated string.
                For ex: if A,B,C,D needs to be removed then col_name must be "A,B,C,D"
        :return: dataframe with filled missing values
        """
        try:
            col_list = []
            for col in col_name:
                col_list.append(col)
            for col in col_list:
                df[col_name].fillna(df[col_name].mean(), inplace=True)
            return df
        except Exception as e:
            return "Error in filling missing values by mean Please check!! Exception is : {}".format(e)

    def fill_missing_val_by_median(self, *col_name):
        """
        Author: Akshat Pant
        This function is used to fill the missing value in the datframe with median imputation
        :param df: name of dataframe whose missing value needs to be filled by median value of the column
        :param  col_name: col_name: name of columns whose missing values need to be filled, any number
                of column names can be passed and the col_name must be passed as comma-seprated string.
                For ex: if A,B,C,D needs to be removed then col_name must be "A,B,C,D"
        :return: dataframe with filled missing values
        """
        try:
            col_list = []
            for col in col_name:
                col_list.append(col)
            for col in col_list:
                df[col_name].fillna(df[col_name].median(), inplace=True)
            return df
        except Exception as e:
            return "Error in filling missing values with median!! Please Check!! Exception is : {}".format(e)

    def fill_missing_val_by_mode(self, col_name):
        """
        Author: Akshat Pant
        This function is used to fill the missing value in the datframe with mode imputation
        :param df: name of dataframe whose missing value needs to be filled by mode value of the column
        :param  col_name: col_name: name of columns whose missing values need to be filled, any number
                of column names can be passed and the col_name must be passed as comma-seprated string.
                For ex: if A,B,C,D needs to be removed then col_name must be "A,B,C,D"
        :return: dataframe with filled missing values
        """
        try:
            col_list = []
            for col in col_name:
                col_list.append(col)
            for col in col_list:
                df[col_name].fillna(df[col_name].mode(), inplace=True)
            return df
        except Exception as e:
            return "Error in filling missing values with mode!! Please Check!! Exception is {}".format(e)

    def standardize_dataframe(self, df):
        """
        Author: Akshat Pant
        This function is used to standardize the dataframe based on standard normal distribution
        i.e. mean=0 and std =1
        :param df:  the datframe to be standardized
        :return:    an array of standardized data
        """
        try:
            std = StandardScaler()
            std_df = std.fit_transform(df)
            return std_df
        except Exception as e:
            return "Error in Standardizing Dataframe!! Please check!! Exception is : {}".format(e)

    def split_train_test(self,df, target_variable, test_size):
        """
        Author: Akshat Pant
        :param df: the dataframe which needs to be split into train and test dataset
        :param target_variable: the output label which needs to be predicted
        :param test_size: size of test data set, this value must lie between 0 to 1
        :return: Training and Testing dataset
                    x_train:    this is feature columns for training dataset
                    x_test:     this is feature columns for test dataset
                    y_train:    this is label column for training dataset
                    y_test:     this is label column for testing datset
        """
        try:
            x = df.drop(target_variable, axis=1)
            y = df[target_variable]
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = test_size)
            return x_train, x_test, y_train, y_test
        except Exception as e:
            return "Error in spliting train and test data!! Please check!! Exception is : {}".format(e)

# p = Preprocessing('../../Advertising.csv')

# print(p.read_csv_file())


# df = p.read_csv_file()
# print(df.head())
# print(p.remove_column_by_name("Unnamed: 0", "newspaper"))
# print(p.remove_column_by_name(df, "Unnamed: 0", "newspaper"))
# print(p.find_missing_values(df))
# print(p.standardize_dataframe(df))
# print(p.split_train_test(df,'sales',0.33))