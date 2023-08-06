import pyinputplus as pyip
from dataframe import DataFrame
import basic

def load(dataset):

    df = DataFrame(dataset).readcsv()

    def studydf(df):
        choice = ["Basic","Advanced","Visualization"]
        action = pyip.inputMenu(choice ,  numbered=True)
        if action == "Basic":
            basic.do(df)
        # elif action == "Advanced":
        #     Advanced.do(df)
        # else:
        #     Visual.do(df)

    while(True):
        decision= pyip.inputMenu(["NO","YES"],prompt="do you want to analyse data", numbered=True)
        if decision == "YES":
            studydf(df)
        else:
            break


#load("D:\data science\ineuron\ML\ML\class\Admission_Prediction.csv")








