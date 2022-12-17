import pandas as pd
import csv
from src import flow_detector

class Compare: 
    def run(self):
        df1 = pd.read_csv("output8.csv",usecols=[0,1],names=['Source IP','Destination IP'])
        df2 = pd.read_csv("C:/Users/Rawan/Desktop/Senior Year/Graduation Project/pintrest ip adresses.csv",usecols=[2,3],names=['Source','Destination'])
        l=df1.isin(df2)
        print(l)
        with open("C:/Users/Rawan/Desktop/Senior Year/Graduation Project/pintrest ip adresses.csv", 'r') as f1, open("output8.csv", 'r') as f2:
            file1 = csv.reader(f1)
            file2 = csv.reader(f2)
            a = {row[0] for row in file2}
            b = {row[2] for row in file1}
        print ("In new  File  but not in whiteList", a - b )
    