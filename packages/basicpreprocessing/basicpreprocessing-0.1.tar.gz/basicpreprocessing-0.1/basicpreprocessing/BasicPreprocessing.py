import pandas as pd
import numpy as np
import logging as lg


class BasicPreprocessing():
    
    def __init__(self,data):
        self.data = data

    def create_logger(self):
        """
        Used to create a logger named 'pre_processing_logger.log'
        """
        try:
            lg.basicConfig(filename='pre_processing_logger.log', level = lg.INFO ,format='%(asctime)s - %(levelname)s - %(message)s')
        except Exception as e:
            print(e)
            
    def load_dataset(self):
        """
            Used load the dataset
            returns dataframe object
        """
        try:
            ai_df = pd.read_csv(self.data)
            lg.info('data loaded successfully!!!')
            return ai_df
        except Exception as e:
            lg.exception(str(e))
           
    def display_sample_rows(self, df):
        """
            Used to display the first 5 rows
            input parameter: dataframe object
            returns dataframe object
        """
        try:
            lg.info('display_sample_rows')
            return df.head()
        except Exception as e:
            lg.exception(str(e))
            
    def find_missing_values(self, df):
        """
            Used to find missing values in each column
            input parameter: dataframe object
            returns series object
        """
        try:
            lg.info('finding missing values !!!')
            return df.isnull().sum()
        except Exception as e:
            lg.exception(str(e))
            
            
    def column_data_types(self, df):
        """
            Used to find data types of columns
            input parameter: dataframe object
            returns series object
        """
        try:
            lg.info('column data types')
            return df.dtypes
        except Exception as e:
            lg.exception(str(e))
            
    def correlation_between_columns(self, df):
        """
            Used to find correlation between columns
            input parameter: dataframe object
            returns series object
        """
        try:
            lg.info('correlation_between_columns')
            return df.corr()
        except Excepton as e:
            lg.exception(str(e))
            
    
