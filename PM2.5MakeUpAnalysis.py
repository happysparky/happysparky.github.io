import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl as op
import seaborn as sns

def extractData(rawData):
    extracted = []
    for i in rawData:
        df = pd.read_csv(i)
        extracted.append(df)
    return extracted


def parseData(rawData):
    parsed = []
    for i in rawData:
        # Read the columns we want
        df = pd.read_csv(i, usecols=["Parameter Name", "Duration Description", "Date (Local)", "Units of Measure",
                                     "Observation Count", "Arithmetic Mean"])

        # Change date to datetime object
        df["Date (Local)"] = pd.to_datetime(df["Date (Local)"])

        # Get rid of wind stuff that we don't care about
        # df = df[~df["Parameter Name"].str.contains("Wind|Sample|Temperature|Pressure|pressure")]

        # list of things to keep
        keepList = ["Average Ambient Pressure", "Nitric oxide (NO)", "Carbon monoxide",
                    "Reactive oxides of nitrogen (NOy)", "Sulfur dioxide", "Ambient Max Temperature",
                    "Average Ambient Temperature", "Oxides of nitrogen (NOx)", "Wind Speed - Scalar",
                    "Barometric pressure", "Wind Direction - Scalar", "NOy - NO", "Nitrogen dioxide (NO2)",
                    "Ozone", "Solar radiation", "Ambient Min Temperature", "Relative Humidity",
                    "Outdoor Temperature", "Ultraviolet radiation", "Average Ambient Temperature for URG3000N",
                    "Average Ambient Pressure for URG3000N", "Wind Direction - Resultant",
                    "Wind Speed - Resultant"]
        df = df[(df["Parameter Name"].str.contains("PM2.5")) |
                (df["Parameter Name"].isin(keepList))]
        parsed.append(df)

    return parsed


# Creates graphs for the first three parameters when a single year is input
def graphByParameter(year):
    grouped = year.groupby('Parameter Name')

    count = 0
    for key in grouped.groups.keys():
        fig = plt.figure()
        plt.plot(grouped.get_group(key)["Date (Local)"],
                 grouped.get_group(key)["Arithmetic Mean"])
        plt.xlabel("Date")
        plt.ylabel("Arithmetic Mean (" +
                   pd.unique(grouped.get_group(key)["Units of Measure"])[0] + ")")
        plt.xticks(rotation=35)
        plt.title("Change in " + key + " Throughout One Year (2016)")
        plt.legend([key])
        count += 1
        if count == 5:
            break

    plt.show()


def graphAll(data):
    # Everything in one plot
    # Really messy and difficult to tell
    # data.set_index("Date (Local)", inplace=True)
    # df = data.groupby(data["Parameter Name"])["Arithmetic Mean"].plot(legend=False)
    # plt.show()

    # Another grouping all on one plot...
    fig, ax = plt.subplots()
    for key, grp in data.groupby(data['Parameter Name']):
        ax.plot(grp["Date (Local)"], grp["Arithmetic Mean"], label=key)

    ax.legend()
    plt.show()

def pivotToYear(years):


    # print(years[0].head())
    # print(years[0]["Parameter Name"].unique())
    count = 0

    for i in range(0, len(years)):

        #years[i] = years[i].groupby(years[i]["Parameter Name"])
        years[i].set_index(["Date (Local)", "Parameter Name"], inplace=True)
        #years[i].set_index(["Date (Local)", "Parameter Name"], inplace=True)
        #print(years[i]["Date (Local)"].tolist())
        #years[i] = years[i].stack()
        #years[i] = years[i].unstack("Parameter Name")
        #years[i] = pd.pivot_table(years[i], index="Date (Local)")

    #why doesn't using a standard for loop work?
    #for year in years:
        # year = year.pivot(index=year["Date (Local)"], columns=year["Parameter Name"])
        # year = year.pivot_table(year, index=year["Date (Local)"], columns=year["Parameter Name"])
        # year = temp

    #years[0].to_excel("output.xlsx")

# input a year
def getStats(data):
    print("Unique particulates: ")
    uniqueParameters = pd.unique(data["Parameter Name"])

    # for i in uniqueParameters:
    #    print(i)
    # print(uniqueParameters)

    print("Has length " + str(len(uniqueParameters)))

    print(data.head())

def heatmap(oneYear):
    cut = pd.DataFrame([oneYear["Parameter Name"], oneYear["Arithmetic Mean"]])
    print(cut)
    corr = cut.corr()
    print(corr)
    #sns.heatmap(corr)
    #plt.show()



def main():
    pd.set_option("max_columns", None)
    allRawData = ["daily_06_037_1103_2016.csv",
                  "daily_06_037_1103_2017.csv",
                  "daily_06_037_1103_2018.csv",
                  "daily_06_037_1103_2019.csv",
                  "daily_06_037_1103_2020.csv"]

    # get rid of wind stuff that we don't care about
    years = parseData(allRawData)
    #getStats(years[0])
    #graphByParameter(years[0])
    #pm25Only = years[0][years[0]["Parameter Name"].str.contains("PM2.5 LC")]
    #graphAll(pm25Only)
    #pivotToYear(years)
    years[0] = years[0].T
    print(years[0])
    #years[0].to_excel("2016Data.xlsx")


#  years[0].columns = years[0].loc["Parameter Name"]




    # years[0] = years[0].groupby(years[0]["Parameter Name"])
    # for key, group in years[0]:
    #     print(key)


# getStats(years[0])


# getStats(parseddf[0])


main()
