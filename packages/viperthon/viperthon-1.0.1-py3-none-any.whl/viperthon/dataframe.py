import pandas as pd


class DataFrame:

    def __init__(self,path):
        self.path = path
        self.delimiter = ','

    def readcsv(self):
        """
        This will load and read your csv file. Provide your datafile here
        :return:
        """
        self.df = pd.read_csv(self.path)
        return self.df
    def readjson(self):
        """
        This will read your json file
        :return:
        """
        self.df = pd.read_json(self.path)
        return self.df


