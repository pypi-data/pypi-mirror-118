import pandas as pd
import seaborn as sns
from termcolor import colored
import matplotlib.pyplot as plt

class eda:
    """ Performs Automatic Exploratory Data Analysis(EDA) for datasets."""
    def __init__(self, df):
        self.df = df

    def sample(self, num_or_rows: int = 10, all_columns: bool = False):
        """Sample of dataset"""
        if all_columns:
            pd.set_option("display.max_columns", None)
        print(colored("\nSample of Dataframe:", "red", attrs=["bold"]))
        print(self.df.sample(num_or_rows))

    def info(self):
        """Information of dataset"""
        print(colored("\nInformation of Dataset:", "red", attrs=["bold"]))
        print(self.df.info())

    def shape(self, formatted_output: bool = True):
        """Shape of dataset"""
        if not formatted_output:
            print("Shape of DataFrame: ", self.df.shape)
            return None
        print(colored(f"\nDataframe contains {self.df.shape[0]} rows and {self.df.shape[1]} columns", "blue", attrs=["bold"]))

    def statistical_summary(self, formatted_output: bool = True):
        """Statistical summary of dataset"""
        if not formatted_output:
            print("\nSummary Statistics of Dataset: \n", self.df.describe())

        print(colored("\nSummmary Statistics of Dataset : ", "red", attrs=["bold"] ))
        print(self.df.describe())

    def get_categorical_columns(self):
        """Return list of categorical features"""
        print(colored("\nCategorical Columns in Dataset:", "red", attrs=["bold"]))
        self.cat_cols = self.df.select_dtypes(include="O").columns.tolist()
        print(self.cat_cols)

    def get_numerical_columns(self):
        """Return list of numerical features"""
        print(colored("\nNumerical Columns in Dataset:", "red", attrs=["bold"]))
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        self.num_cols = self.df.select_dtypes(include=numerics).columns.tolist()
        print(self.num_cols)

    def missing_values_info(self):
        """Missing Value information"""
        print(colored("\nMissing Value Information of Dataset:", "blue", attrs=["bold"]))       
        if self.df.isnull().sum().sum() > 0:
            null_df = pd.DataFrame(self.df.isnull().sum()).reset_index()
            null_df.columns = ["column_name", "null_rows"]
            null_df["null_percentage"] = null_df["null_rows"]*100 / df.shape[0]
            null_df = null_df[null_df["null_percentage"] != 0].sort_values(
                "null_percentage", ascending=False).reset_index(drop=True)
            print(colored(f"\nThere are total {null_df.shape[0]} columns having null values out of {self.df.shape[1]} columns in dataframe\n", "red", attrs=["bold"]))
            print(null_df)
            
        else:
            print(colored(
                "\nCongrats!!, The Dataframe has NO NULL VALUES\n", "green", attrs=["bold"]))
        
    def duplicate_rows(self):
        """Find Duplicated rows in dataset"""
        print(colored("\nDuplicate Rows in Dataset:", "red", attrs=["bold"]))
        if(self.df.duplicated().sum()) > 0:
            print(colored(f"\nThe Dataframe has {self.df.duplicated().sum()} Duplicate Rows\n", "green", attrs=["bold"]))
        else:
            print(colored("\nThe Dataframe has NO DUPLICATE ROWS.\n", "green", attrs=["bold"]))

    def correlation(self):
        """This method is to find the pairwise correlation of all columns in the dataframe. """
        print(colored("\nCorrelation of Dataset:", "red", attrs=["bold"]))
        print(self.df.corr())
        print(colored("\nCorrelation Heatmap Plot:\n", "red", attrs=["bold"]))
        sns.heatmap(df.corr(), annot=True, linewidth=3)
        plt.show()


class eda_report:
    '''This class generates EDA report'''
    def __init__(self, df):
        self.df = df
        self.unique_df = pd.DataFrame()
        self.obj_eda = eda(self.df)
        self.obj_eda.shape()
        self.obj_eda.sample()
        self.obj_eda.get_categorical_columns()
        self.obj_eda.get_numerical_columns()
        self.obj_eda.missing_values_info()
        self.obj_eda.duplicate_rows()
        self.obj_eda.statistical_summary()
        self.obj_eda.info()
        self.obj_eda.correlation()


# Example code
if __name__ == "__main__":
    df = sns.load_dataset('tips')
    report = eda_report(df)
    print(report)



