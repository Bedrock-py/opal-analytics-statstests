
import subprocess
import os
from bedrock.analytics.utils import Algorithm
import pandas as pd
import logging
import statsmodels.api as sm
import csv
import scipy.stats as stats

class Wilcoxon(Algorithm):
    def __init__(self):
        super(Wilcoxon, self).__init__()
        self.parameters = []
        self.inputs = ['x_data.csv','x_features.txt','y_data.csv','y_features.csv']
        self.outputs = ['matrix.csv']
        self.name ='Wilcoxon'
        self.type = 'stats'
        self.description = 'Performs Either Wilcoxon Signed-Rank or rank-sums test'
        self.parameters_spec = [
            { "name" : "x_column", "attrname" : "x_column", "value" : "x.column_name", "type" : "input" },
            { "name" : "y_column", "attrname" : "y_column", "value" : "y.column_name", "type" : "input" },
            { "name" : "paired", "attrname" : "paired" , "value" : "False", "type" : "input"}
        ]

    def __build_df__(self, rootpath):
        featuresPath = rootpath + 'features.txt'
        matrixPath = rootpath+ 'matrix.csv'
        df = pd.read_csv(matrixPath, header=-1)
        featuresList = pd.read_csv(featuresPath, header=-1)

        df.columns = featuresList.T.values[0]

        return df

    def compute(self, filepath, **kwargs):
        x_df = self.__build_df__(filepath['x_data.csv']['rootdir'])

        if 'y_data.csv' not in filepath or 'rootdir' not in filepath['y_data.csv']:
            y_df = pd.DataFrame()
        else:
            y_df = self.__build_df__(filepath['y_data.csv']['rootdir'])

        x_base, x_columnname = self.x_column.split(".", 1)
        y_base, y_columnname = self.y_column.split(".", 1)

        if x_base == "x":
            x_data = x_df[x_columnname]
        elif x_base == "y":
            x_data = y_df[x_columnname]
        else:
            logging.error("Invalid Base Matrix for x")
            return None

        if y_base == "x":
            y_data = x_df[y_columnname]
        elif y_base == "y":
            y_data = y_df[y_columnname]
        else:
            logging.error("Invalid Base Matrix for y")
            return None

        if self.paired.lower() == "true":
            results = stats.wilcoxon(x_data, y_data)
            summary = [
                ["statistic", results[0]],
                ["pvalue", results[1]]
            ]
        elif self.paired.lower() == "false":
            results = stats.ranksums(x_data, y_data)
            summary = [
                ["statistic", results[0]],
                ["pvalue", results[1]]
            ]
        else:
            logging.error("Invalid Paired choice")
            return None

        self.results = {'matrix.csv': summary}
