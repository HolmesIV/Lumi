import pandas as pd
import numpy as np
from pathlib import Path
from config import *
from lib import objs

pd.options.display.width = 10

def categorize_ingredient(ingredient):
    if type(ingredient) != str:
        return "Undefined"
    for category in objs.reg_dict:
        regex_list = objs.reg_dict[category]
        for regex in regex_list:
            if regex.match(ingredient):            
                return category
    return "Undefined"

def split_ID(ID):
    if type(ID) != str:
        return ("", "")
    return ID.split(sep="_")

def database_to_df(db_filepath):
    cols = ["Project", "Request", "Requester", "Batch", "Sample Description", "Ing_ID", "Ing_pct"]

    db = pd.read_excel(db_filepath, header=None)
    db_recipe = db.copy().iloc[:423].dropna(how="all")
    db_recipe[0].fillna(method="ffill", inplace=True)
    db_recipe[1].fillna(method="ffill", inplace=True)

    # Separate out ingredient metadata to merge later
    db_ings = db_recipe.iloc[6:, :6].drop(2, axis=1)
    db_ings[0] = list(map(lambda x: str(x).strip(), db_ings[0]))
    db_ings.columns = ["Function", "Sub-Group", "Ingredient", "Ing_PLM", "Ing_Description"]
    db_ings.insert(0, "Ing_ID", db_ings.index)

    # Transform datatable to format of request x ingredient
    db_recipe = db_recipe.T
    db_recipe = db_recipe.drop(range(6)).drop(5, axis=1)
    db_recipe = pd.melt(
        db_recipe,
        id_vars=[0,1,2,3,4],
        var_name="Ing_ID",
        value_name="Ing_pct",    
    )

    db_recipe.columns = cols
    db_recipe = db_recipe.drop(0).dropna(subset=["Ing_pct"])
    db_recipe.dropna(how="all", subset=["Request", "Batch"], inplace=True)

    # Add ingredient information back in
    db_recipe = db_recipe.merge(db_ings, on="Ing_ID", how="left")
    for column in cols[:-2]:
        db_recipe[column] = list(map(lambda x: str(x).strip(), db_recipe[column]))
    db_recipe.drop("Ing_ID", axis=1, inplace=True)

    return db_recipe


def lims_recipes_to_df(filepath):
    cols = ["Request", "Batch", "Sample", "Product", "Expected_Batch_Size", "Expected_Batch_Size_Units",
            "Ing_ID", "Ingredient", "Ing_pct", "Ing_Target_Amt", "Ing_Actual_Amt", "Ing_Units",
            ]
    lims_recipe = pd.read_excel(filepath, header=0)
    lims_recipe.columns = cols
    lims_recipe = lims_recipe[cols[:-3]]
    lims_recipe.dropna(subset=["Ingredient", "Ing_pct"], inplace=True)
    ingredient_names = lims_recipe["Ingredient"]
    lims_recipe["Function"] = list(map(categorize_ingredient, ingredient_names))


    return lims_recipe

def concat_tables(lims_table, db_table, print=False, filepath=None):
    concatted = pd.concat([lims_table, db_table], ignore_index=True)
    if print and filepath:
        concatted.to_excel(filepath + "full_recipe_list.xlsx", sheet_name="Ingredient_List")
    return concatted

def generate_NN_table(dataframe):
    
    nndf = dataframe[["ID", "Request", "Function", "Ing_pct"]]
    nndf = nndf.groupby(["ID", "Request", "Function"]).sum().reset_index()
    nndf = nndf.merge(nndf, how='left', on="Function")
    nndf.columns = ["ID", "Request", "Function", "Ing_pct", "Comp_ID", "Comp_Request", "Comp_Ing_pct"]
    nndf = nndf.assign(Delta=lambda x: (x["Ing_pct"] - x["Comp_Ing_pct"]) ** 2)
    nndf = nndf.groupby(by=["ID", "Comp_ID"]).sum(numeric_only=True).reset_index()
    nndf = nndf.assign(Distance=lambda x: np.sqrt(x["Delta"])).sort_values(by="Distance")
    nndf = nndf[["ID", "Comp_ID", "Distance"]]
    
    return nndf

def main():
    folder_fp = env_folder + "files/"

    if Path(folder_fp + old_datatable_output_filename).exists():
        db_recipe_list = pd.read_excel(folder_fp + old_datatable_output_filename)
    else:
        db_recipe_list = database_to_df(folder_fp + old_datatable_filename)
        db_recipe_list.to_excel(folder_fp + old_datatable_output_filename, index=False)

    lims_recipe_list = lims_recipes_to_df(folder_fp + lims_datatable_filename)
    
    if Path(folder_fp + "full_recipe_list.xlsx").exists():
        full_recipe_list = pd.read_excel(folder_fp + "full_recipe_list.xlsx", index_col=0)
    else:
        full_recipe_list = concat_tables(lims_recipe_list, db_recipe_list, print=True, filepath=folder_fp)
    
    full_recipe_list = full_recipe_list.assign(ID=lambda x: x["Request"] + "_" + x["Batch"])
    
    nndf = generate_NN_table(full_recipe_list)
    nndf.to_excel(folder_fp + "nearest_neighbor.xlsx", sheet_name="NN_List")

if __name__ == '__main__':
    main()