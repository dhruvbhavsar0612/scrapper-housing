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
                X.columns[0]:'Sr No',
                X.columns[1]:'Document No',
                X.columns[2]:'Document Type',
                X.columns[3]:'D.N. Office',
                X.columns[5]:'Buyer Name',
                X.columns[6]:'Seller Name',
            }
        )
        return X_renamed

class DateFormat(BaseEstimator, TransformerMixin):
    def fit(self, X,  y=None):
        return self
    
    def transform(self, X):
        try:
            X['Year'] = pd.to_datetime(X['Year'], format='%d/%m/%Y')
        except ValueError as e:
            print(e)
        return X

class FloatInt(BaseEstimator, TransformerMixin):
    def fit(self, X,  y=None):
        return self
    
    def transform(self, X):
        return X.astype({col: 'int32' for col in X.columns if X[col].dtype == 'float64'})