from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

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