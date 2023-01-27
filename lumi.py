import pandas as pd
from math import sqrt

def get_ID_by_request(request):
    return df_meta["Request_Number"].loc[lambda x: x == request].index[0]

def get_request_by_ID(id):
    try:
        req_number = df_meta["Request_Number"].iloc[id]
    except IndexError:
        # print(f"Index Error for {id}")
        return None
    
    return req_number

def euc_dist(recipe_ID, comp_ID):
    return sqrt( ((df_grouped[recipe_ID] - df_grouped[comp_ID]) ** 2).sum() )

def get_NN_obj_by_ID(id, dataframe):
    eucs = {
                i : 
                {
                    "Value": euc_dist(id, i),
                    "Request": get_request_by_ID(i),
                }
                for i in dataframe if type(i) == int
            }
    
    return dict(sorted(eucs.items(), key = lambda item: item[1]["Value"]))

def get_NN_df_by_ID(id, dataframe):
    array = [["ID", "Request", "Value"]]
    for i in dataframe:
        if type(i) == int:
            array.append([i, get_request_by_ID(i), euc_dist(id, i)])
    return array

def generate_excel_tables(filepath):
    #filepath = "C:/Users/Paul.Barron/LumiEnv/Lumi/files/Lumi_DB.xlsx"
    df = pd.read_excel(filepath, header=None)
    df.dropna(how="all", inplace=True)

    df_meta = df.copy()
    df_ings = df.copy()
    df_stab = df.copy()
    df_recs = df.copy()

    # Meta data
    df_meta = df_meta.iloc[0:4, 7:].T
    df_meta.columns = ["Project", "Request_Number", "Requester", "Batch_Number"]
    df_meta["Batch_Number"] = list(map(lambda x : str(x).strip(), df_meta["Batch_Number"]))
    df_meta["Requester"] = list(map(lambda x : str(x).strip(), df_meta["Requester"]))

    # Ingredients
    df_ings.columns = df_ings.iloc[5]
    df_ings = df_ings.iloc[6:373, 0:7]
    df_ings.insert(0, "Ing_ID", df_ings.index)
    df_ings.fillna(method="ffill", inplace=True)
    df_stab = df.copy()
    df_stab = df_stab.iloc[382:, 6:].T
    df_stab.columns = df_stab.iloc[0]
    df_stab.insert(0, "ID", df_stab.index)
    df_stab = df_stab.iloc[1:, :8]

    # Recipes
    df_recs = df_recs.iloc[6:373, 7:]
    df_recs.insert(0, "Ing_ID", df_recs.index)
    df_recs = df_recs.merge(df_ings, on="Ing_ID", how="left")
    df_recs = df_recs.iloc[:, :-6]
    df_recs.insert(1, "Function", df_recs.pop("Function"))

    # Recipes grouped by ingredient
    df_grouped = df_recs.groupby("Function").sum(numeric_only=False)

    req_num = "R-20220118-00041"
    req_id = get_ID_by_request(req_num)
    result = get_NN_list_by_ID(req_id, df_grouped)
    print(result)

    return 0
