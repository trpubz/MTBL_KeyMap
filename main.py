"""
Automates the gathering of MTBL's Fantasy Player Key Map.
Houses ESPN, Fangraphs, Savant, Baseball-Reference IDs.
v 1.0.0
modified: 12 JUN 2023
by pubins.taylor
"""
import os
import json

import pandas as pd

mtblDir = "/Users/Shared/BaseballHQ/resources/extract/"


def fetchPlayerKeyMap(url):
    df = pd.read_html(url, header=1, index_col=None)[
        0]  # returns a list of dataframes, so we need to index the first one, header is set to the second row
    print("Key Map pulled from the interwebs")
    df.drop(columns=df.columns[0],
            inplace=True)  # drop the first column, which is the html index column, this uses pandas indexing
    df.drop(index=0, inplace=True)  # drop the first row, which is NaN
    # print(f"{df.count} number of players before dropping empty values")
    df.dropna(subset=["MLBID", "ESPNID"], inplace=True)
    # print(f"{df.count} number of players after dropping empty values")
    # drop all rows that have NaN in the ESPNID column
    df = df.astype({"ESPNID": int, "MLBID": int})  # casting from float to str requires int as an intermediate step
    df = df.astype({"ESPNID": str, "MLBID": str})

    # Convert the dataframe to a JSON string
    json_str = df.to_json(orient="records")
    # Parse the JSON string into a Python dictionary and pretty-print it
    parsed = json.loads(json_str)
    pretty_json = json.dumps(parsed, indent=2, sort_keys=False)
    writeOut(dir=mtblDir, fileName="mtblKeyMap", ext=".json", content=pretty_json)


def writeOut(dir: str = "", fileName: str = "", ext: str = "", content: str = "") -> None:
    with open(os.path.join(dir, (fileName + ext)), mode='w+', encoding='utf-8') as f:
        # print(content, file=f)
        f.write(content)
        print(f'{fileName}{ext} successfully saved to {dir}')
        f.close()


def main():
    print("\n---Starting MTBL Key Map Fetch---\n")
    mtblsURL = "https://docs.google.com/spreadsheets/d/e/2PACX" \
               "-1vSEw6LWoxJrrBSFY39wA_PxSW5SG_t3J7dJT3JsP2DpMF5vWY6HJY071d8iNIttYDnArfQXg-oY_Q6I/pubhtml?gid=0" \
               "&single=true"
    fetchPlayerKeyMap(mtblsURL)
    print("\n---Finished MTBL Key Map Fetch---")


if __name__ == '__main__':
    main()
