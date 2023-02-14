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
    db_ings[0] = db_ings[0].str.strip()
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
    db_recipe = db_recipe.drop(0)
    db_recipe.dropna(how="all", subset=["Request", "Batch"], inplace=True)
    db_recipe["Ing_pct"].fillna(0, inplace=True)

    # Add ingredient information back in
    db_recipe = db_recipe.merge(db_ings, on="Ing_ID", how="left")
    for column in cols[:-2]:
        db_recipe[column] = db_recipe[column].str.strip()
    db_recipe.drop("Ing_ID", axis=1, inplace=True)

    return db_recipe


def lims_recipes_to_df(filepath):
    cols = ["Request", "Batch", "Sample", "Product", "Expected_Batch_Size", "Expected_Batch_Size_Units",
            "Ing_ID", "Ingredient", "Ing_pct", "Ing_Target_Amt", "Ing_Actual_Amt", "Ing_Units",
            ]
    lims_recipe = pd.read_excel(filepath, header=0)
    lims_recipe.columns = cols
    lims_recipe = lims_recipe[cols[:-3]]
    lims_recipe.dropna(subset=["Ingredient"], inplace=True)
    ingredient_names = lims_recipe["Ingredient"]
    lims_recipe["Function"] = list(map(categorize_ingredient, ingredient_names))
    lims_recipe["Ing_pct"].fillna(0, inplace=True)

    return lims_recipe

def concat_tables(lims_table, db_table, output_file=False, filepath=None):
    concatted = pd.concat([lims_table, db_table], ignore_index=True)
    concatted["Batch"].fillna("", inplace=True)
    concatted = concatted.assign(ID=lambda x: x["Request"] + "_" + x["Batch"])

    for column in concatted.columns:
        if concatted[column].dtype == "object":
            concatted[column] = concatted[column].str.strip()
    
    concatted = concatted.replace(r'\n', ' ', regex=True)

    if output_file and filepath:
        concatted.to_csv(filepath + full_recipe_list_filename)
    
    print(concatted)
    
    return concatted

def generate_NN_table(nndf):
    
    # Ensure each recipe has the same number of ingredients, filling '0' where there is no value.
    nndf = nndf[["ID", "Function", "Ing_pct"]]
    nndf = nndf.groupby(["ID", "Function"]).sum().reset_index()
    nndf = nndf.pivot(index="ID", columns="Function", values="Ing_pct").fillna(0).reset_index()
    nndf = pd.melt(
        nndf,
        id_vars="ID",
        var_name="Function",
        value_name="Ing_pct"
    )

    # Merge datatable with itself and calculate euclidian distance
    nndf = nndf.merge(nndf, how="left", on="Function", suffixes=(None, "_comp"))
    nndf = nndf.assign(Delta=lambda x: np.square(x["Ing_pct"] - x["Ing_pct_comp"]))
    nndf = nndf.groupby(by=["ID", "ID_comp"]).sum(numeric_only=True).reset_index()
    nndf = nndf.assign(Distance=lambda x: np.sqrt(x["Delta"])).drop("Delta", axis=1)[["ID", "ID_comp", "Distance"]]

    # Export to excel
    nndf.to_excel(files_fp + nn_filename, sheet_name="NN_List")

    return nndf

def main():
    pd_settings()

    if Path(files_fp + full_recipe_list_filename).exists():
        full_recipe_list = pd.read_csv(files_fp + full_recipe_list_filename, index_col=0, low_memory=False)
    else:
        if Path(files_fp + old_datatable_output_filename).exists():
            db_recipe_list = pd.read_csv(files_fp + old_datatable_output_filename)
        else:
            db_recipe_list = database_to_df(files_fp + old_datatable_filename)
            db_recipe_list.to_csv(files_fp + old_datatable_output_filename, index=False)

        
        if Path(files_fp + lims_recipe_modified).exists():
            lims_recipe_list = pd.read_csv(files_fp + lims_recipe_modified)
        else:
            lims_recipe_list = lims_recipes_to_df(files_fp + lims_datatable_filename)
            lims_recipe_list.to_csv(files_fp + lims_recipe_modified, index=False)


        full_recipe_list = concat_tables(lims_recipe_list, db_recipe_list, output_file=True, filepath=files_fp)
    
    generate_NN_table(full_recipe_list)

if __name__ == '__main__':
    main()