from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
from Constants.constants import TYPE_MAPPING, VALID_TYPES

def split_names(row):
    '''
    input-
        row(str): row from the table
    output-
        name(str): name of the buyer or seller
    '''
    try:
        import re
        import string
        # Split the row based on the pattern '\d+\)'
        names = re.split(r'\d+\)', row)
        # Remove leading and trailing spaces from each name
        names = [name.strip() for name in names if name.strip()]
        
        name = names[0].strip(string.whitespace + string.punctuation)
        return name
    except IndexError as e:
        return np.nan
    
def split_info(row):
    '''
    input-
        row(str): row from the table
    output-
        name(str): name of the buyer or seller
    '''
    try:
        import re
        import string
        # Split the row based on the pattern '\d+\)'
        names = re.split(r'\d+\)', row)
        # Remove leading and trailing spaces from each name
        names = [name.strip() for name in names if name.strip()]
        
        name = names[0].strip(string.whitespace + string.punctuation + 'Other Information:')
        return name
    except IndexError as e:
        return np.nan


# CLASSES for specific task pipelines

class NanDropper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X.dropna(axis=0)

class ColDropper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self,X):
        return X.drop(X.columns[-2], axis=1)
    
class ReplaceNames(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_renamed = X.rename(columns = {
                X.columns[0]:'sr_no',
                X.columns[1]:'doc_no',
                X.columns[2]:'doc_type',
                X.columns[3]:'dn_office',
                X.columns[4]:'doc_date',
                X.columns[5]:'buyer_name',
                X.columns[6]:'seller_name',
                X.columns[7]:'other_info',
                X.columns[8]:'list_no_2'
            }
        )
        return X_renamed

class DateFormat(BaseEstimator, TransformerMixin):
    def fit(self, X,  y=None):
        return self
    
    def transform(self, X):
        try:
            X['doc_date'] = pd.to_datetime(X['doc_date'], format='%d/%m/%Y')
        except ValueError as e:
            print(e)
        return X

class FloatInt(BaseEstimator, TransformerMixin):
    def fit(self, X,  y=None):
        return self
    
    def transform(self, X):
        return X.astype({col: 'int32' for col in X.columns if X[col].dtype == 'float64'})
    
class NameSeparator(BaseEstimator, TransformerMixin):
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X['latest_buyer_name'] = X['buyer_name'].apply(split_names)
        X['latest_seller_name'] = X['seller_name'].apply(split_names)
        X['other_info'] = X['other_info'].apply(split_info)
        return X

class HistoryColumns(BaseEstimator, TransformerMixin):
    def fit(self,X,y=None):
        return self
    
    def transform(self, X):
        X = X.rename(columns={'buyer_name': 'buyer_history', 'seller_name': 'seller_history'})
        return X

class RemoveAnomalies(BaseEstimator, TransformerMixin):
    def fit(self,X,y=None):
        return self
    
    def transform(self, X):
        X['doc_type'] = X['doc_type'].str.lower()
        X['doc_type'] = X['doc_type'].replace(TYPE_MAPPING)

        X = X[X['doc_type'].isin(VALID_TYPES)]
        return X