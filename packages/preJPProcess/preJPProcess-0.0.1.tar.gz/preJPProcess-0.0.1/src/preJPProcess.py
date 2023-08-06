# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 14:16:15 2021

@author: jbhatt
"""

from sklearn.preprocessing import StandardScaler

class preJPProcess():
    
    """
    To initialize:
        
    e.g  p = preProcess(dataFrame)
    
    A class used to represent an Pre Processing of Data Frame.

    ...

    Attributes
    ----------
    df : DataFrame
        pandas.DataFrame
        class pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)[source]
            Two-dimensional, size-mutable, potentially heterogeneous tabular data.

            Data structure also contains labeled axes (rows and columns). Arithmetic operations align on both row and column labels. Can be thought of as a dict-like container for Series objects. The primary pandas data structure.

        Parameters
            datandarray (structured or homogeneous), Iterable, dict, or DataFrame
                    Dict can contain Series, arrays, constants, dataclass or list-like objects. If data is a dict, column order follows insertion-order.

                    Changed in version 0.25.0: If data is a list of dicts, column order follows insertion-order.

            indexIndex or array-like
                    Index to use for resulting frame. Will default to RangeIndex if no indexing information part of input data and no index provided.

            columnsIndex or array-like
                    Column labels to use for resulting frame when data does not have them, defaulting to RangeIndex(0, 1, 2, …, n). If data contains column labels, will perform column selection instead.

            dtypedtype, default None
                    Data type to force. Only a single dtype is allowed. If None, infer.

            copybool or None, default None
                        Copy data from inputs. For dict data, the default of None behaves like copy=True. For DataFrame or 2d ndarray input, the default of None behaves like copy=False.
   
    Methods
    -------
    preProcessData()
       Removes the null values from your dataframe.
    
    scaling()
         Standard Scaling of dataframe
    """

    def __init__(self,df):
        self.df = df
        
    def preProcessData(self):
        print("Null values present in your data : ", self.df.isna().sum())
        print("Preprocessing the data, removing Null Values....")
        columns = self.df.columns
        for col in columns:
            print("Processing : " , col)
            self.df[col].fillna(self.df[col].mean(),inplace=True)
        return self.df
    
    def scaling(self):
        print("Scaling you data")
        columns = self.df.columns
        scalar = StandardScaler()
        for col in columns:
            print("Processing : " , col)
        self.df = scalar.fit_transform(self.df)
        return self.df