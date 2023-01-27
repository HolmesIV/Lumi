import os
import pandas as pd
from openpyxl import Workbook
from pathlib import Path
from time import time

# Variables
directory = "//162.87.125.229/trumbull_data/AMS/Lumisizer/Batches/"

# directory = "C:\\Users\\Paul.Barron\\Downloads"
fileTypes = [".csv", ".xlsx"]
columnNames = {
    "RECIPE"      : "Parent Recipe or Specification",
    "BATCH"       : "Batch",
}

meta_data_titles = ["Project", "Request ID", "Requestor", "Requester", "Batch or Lot#", "Recipe Description"]

db_filepath = "C:/Users/Paul.Barron/LumiEnv/Lumi/\
files/Stability UCQ Lumisizer DSC Formulation Final_NN.xlsx"

class Batch:
    def __init__(self, filepath):
        self.path = filepath
        self.directory = Path(filepath).parent
        self.filename = Path(filepath).name
        self.ext = Path(self.filename).suffix
        self.name = self.filename.removesuffix(self.ext)
        self.recipe = {}
        self.meta_data = {}

def create_batch(filepath):
    if Path(filepath).is_dir():
        files = os.listdir(filepath)
        return {i: Batch(os.path.join(filepath, file)) for i, file in enumerate(files)
                if Path(file).suffix in fileTypes}

    return {0: Batch(filepath)}

def create_data_frames(batches):
    for i, batch in batches.items():
        if batch.ext == ".csv":
            batch.df = pd.read_csv(batch.path)
            recipeCol = columnNames["RECIPE"]
            batchCol = columnNames["BATCH"]

            if recipeCol in batch.df.columns:
                idx = batch.df.columns.get_loc(recipeCol)
                batch.specification = batch.df.at[1, recipeCol]
                batch.df.drop(batch.df.columns[idx], axis = 1, inplace = True)
                            
            if batchCol in batch.df.columns:
                idx = batch.df.columns.get_loc(batchCol)
                batch.batchNo = batch.df.at[1, batchCol]
                batch.df.drop(batch.df.columns[idx], axis = 1, inplace = True)

    return 

def read_data_table(filepath, column):
    
    this_batch = Batch(filepath)
    df = pd.read_excel(filepath, header = None)
    print(df)
    
    for i in range(6):
        item = df.iat[i, 0]
        value = str(df.iat[i, column]).strip()
        if item in meta_data_titles:
            this_batch.meta_data.update({df.iat[i, 0]: value})
    print(this_batch.meta_data) 
    

    df.iat[5, column] = request_no = this_batch.meta_data["Request ID"]
    df.columns = df.iloc[5]
    columns = ["Ingredient", "PLM/GAB/NA Spec #", "Item Desc.", request_no]
    df = df[columns]
    df = df.dropna(subset = df.columns[[0,3]]).drop([0,5])
    # df.drop([0,5], inplace=True)
    this_batch.df = df

    return this_batch

def df_to_excel(batch, directory=False):
    
    if not directory:
        directory = batch.directory
    filepath = f'{batch.directory}\{batch.meta_data["Request ID"]}.xlsx'
    batch.df.to_excel(filepath)
    csv_file = Workbook(filepath)

def print_range(database_file, start=0, end=0):
    if not end:
        return
    for i in range(start, end):
        batch = read_data_table(database_file, i)
        df_to_excel(batch)
        

def main():
    print_range(db_filepath, start=10, end=11)
    return


if __name__ == '__main__':
    start = time()
    main()
    end = time()
    print(f"Time elapsed; {(end - start) * 1000}ms")
    
