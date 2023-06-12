"""
Automates the gathering of MTBL's Fantasy Player Key Map.
Houses ESPN, Fangraphs, Savant, Baseball-Reference IDs.
v 0.1.0
modified: 12 JUN 2023
by pubins.taylor
"""
import os

import pandas as pd


def fetchPlayerKeyMap(url) -> pd.DataFrame:
    # check to see if tempPlayerKeyMap.json exists before proceeding
    # if it does, then read it in and return it
    # if it doesn't, then fetch the data and write it out to a json file
    # then return the dataframe
    filename = "tempPlayerKeyMap.json"
    if os.path.isfile(filename):
        df = pd.read_json(filename, convert_axes=False)
        # specify the columns ESPNID, IDFANGRAPHS, MLBID as strings
        df = df.astype({"ESPNID": str, "MLBID": str})
        # print(df)
        print(f"{filename} exists, returning dataframe")
        return df
    else:
        df = pd.read_html(url, header=1, index_col=None)[
            0]  # returns a list of dataframes, so we need to index the first one, header is set to the second row
        df.drop(columns=df.columns[0],
                inplace=True)  # drop the first column, which is the html index column, this uses pandas indexing
        df.drop(index=0, inplace=True)  # drop the first row, which is NaN
        # print(f"{df.count} number of players before dropping empty values")
        df.dropna(subset=["MLBID", "ESPNID"], inplace=True)
        # print(f"{df.count} number of players after dropping empty values")
        # drop all rows that have NaN in the ESPNID column
        df = df.astype({"ESPNID": int, "MLBID": int})  # casting from float to str requires int as an intermediate step
        df = df.astype({"ESPNID": str, "MLBID": str})
        df.to_json(filename, orient="records")
        # print(df)
        print("Key Map pulled from the interwebs, returning dataframe")
        return df


def main():
    mtblsURL = "https://docs.google.com/spreadsheets/d/e/2PACX" \
               "-1vSEw6LWoxJrrBSFY39wA_PxSW5SG_t3J7dJT3JsP2DpMF5vWY6HJY071d8iNIttYDnArfQXg-oY_Q6I/pubhtml?gid=0" \
               "&single=true"
    df = fetchPlayerKeyMap(mtblsURL)
    print(df)


if __name__ == '__main__':
    main()
