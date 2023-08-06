"""
Dataset information for the data mining.
"""

# Author: Dinesh Naik <dinesh.naik@gmail.com>

import pandas as pd
import numpy as np
import matplotlib as plt


class datainfo():
    def __init__(self):
        """
        Initialize dataframe dataset to explore the data
        """

    def valuetable(self, df):

        """
        Description : This method will create dataframe for each of the column value.
        Dataframe column would be Column Name, Data Type, Value Count, Null Value, Null Value(%), Unique Value

        :param df: pandas dataframe

        :return dataset : dataframe table with the value information like null count, unique value...
        """
        dataset = pd.DataFrame()

        #Create new dataframe column with DF Column
        dataset['Column Name'] = [col for col in df.columns]

        #Create new dataframe column with datatype
        dataset['Data Type'] = [col for col in df.dtypes[df.columns]]

        #New dataframe column with column value count
        dataset['Value Count'] = [cnt for _,cnt in enumerate(df.notnull().sum())]

        #New dataframe column with null value count
        dataset['Null Value'] = [cnt for _,cnt in enumerate(df.isnull().sum())]

        #New dataframe column with null value count
        dataset['Null Value(%)'] = dataset.apply(lambda row: round(row['Null Value']*100/(row['Value Count']+row['Null Value']),2), axis=1)

        #New dataframe column with Unique value count
        dataset['Unique Value'] = [df[col].nunique() for col in df.columns]

        return dataset

    def nullvaluechart(self, df, plotwidth=10, plotheight=5, xlabelrotation=90, textfontsize=10, percent=True):
        """

        Description : This method will represent the stacked bar chart with non null value count and null value count,

        :param df: pandas dataframe
        :param plotwidth: int, widths of the plot area
        :param plotheight: int, height of the plot area
        :param xlabelrotation: int, degree of the text for x label
        :param percent: boolean (defalut=True), If value is True, then null value count represent in percent(%) else count value.
        :param textfontsize: int, text font size for bar patches

        :return: Stacked bar chart with null value count
        """

        df_table = self.valuetable(df)

        if percent == False:
            ax = df_table[['Value Count','Null Value']].plot(kind='bar',stacked=True, figsize=(plotwidth,plotheight))
        else:
            ax = df_table[['Column Name','Null Value(%)']].plot(kind='bar', figsize=(plotwidth,plotheight))

        for i, rect in enumerate(ax.patches):

            if (len(df_table)>i):
                #we can get the chart details
                height = rect.get_height()
                width = rect.get_width()
                x = rect.get_x()
                y = rect.get_y()

                #Lable text to print on the bar chart
                lebel_text = ' ' + str(height)+' - ' + str(df_table['Data Type'][i])
                label_x = x+width/2
                label_y = y+height/2


                if height >0.001:
                    if percent == False:
                        ax.text(label_x,label_y, lebel_text, ha='center', va='center',rotation=90,size=textfontsize,color='white')
                    else:
                        ax.text(rect.get_x() + rect.get_width()/2,1.05*height, lebel_text, ha='center', va='bottom',rotation=90,size=textfontsize,color='black')

        ax.set_xticklabels(df_table['Column Name'],rotation=xlabelrotation,size=12)

        if percent == False:
            ax.legend(loc='best')
            ax.set_xlabel('Column Name',size=15)
            ax.set_ylabel('Count',size=15)
        else:
            ax.legend(['Null Value(%)'],loc='best')
            ax.set_xlabel('Label Name',size=15)
            ax.set_ylabel('% Count',size=15)
            #plt.ylim(0,100)
