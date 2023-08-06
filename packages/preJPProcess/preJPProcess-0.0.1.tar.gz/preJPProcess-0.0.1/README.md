#Preprocessing 

This is one basic project , which pre processes the data frame , removing null values and performs standard scaling.

#Main Features

Removes Null values from DataFrame and do standard Scaling of data


#Installation

pip install preJProcess


#Usage 

e.g, p = preProcess(df)
     df ==> dataFrame
     p.preProcessData()
	 p.scaling()


#Sample Code
from sklearn.preprocessing import StandardScaler

class preProcess():
    def __init__(self,df):
        self.df = df
        
    def preProcessData(self):
        print("Null values present in your data : ", self.df.isna().sum())
        print("Preprocessing the data, removing Null Values....")
        columns = self.df.columns
        scalar = StandardScaler()
        for col in columns:
            print("Processing : " , col)
            self.df[col].fillna(self.df[col].mean(),inplace=True)
        return self.df
	.....
    
