import os
import pandas as pd
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

metaDataTitles = ["Request ID", "Requestor", "Requester", "Batch or Lot#", "Recipe Description"]

db_filepath = "C:/Users/Paul.Barron/LumiEnv/Lumi/\
files/Stability UCQ Lumisizer DSC Formulation Final_NN.xlsx"

class Batch:
    def __init__(self, directory, filename):
        self.path = os.path.join(directory, filename)
        self.directory = directory
        self.filename = filename
        self.ext = Path(self.filename).suffix
        self.name = filename.removesuffix(self.ext)
        self.recipe = {}
        self.meta_data = {}

def isFile(directory, file): # REMOVE IF NOT USED
    return os.path.isfile(os.path.join(directory, file))

def createBatch(filepath):
    if Path(filepath).is_dir():
        files = os.listdir(filepath)
        return {i: Batch(directory, file) for i, file in enumerate(files)
                if Path(file).suffix in fileTypes}

    return {0: Batch(Path(filepath).name)}

def createDataFrames(batches):
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

def readDataTable(filepath, column):
    
    df = pd.read_excel(filepath)
    this_batch = Batch(Path(filepath).parent, Path(filepath).name)

    for i in range(5):
        item = df.iat[i, 0]
        value = df.iat[i, column].strip()
        if item in metaDataTitles:
            this_batch.meta_data.update({df.iat[i, 0]: value})

    L_df = pd.read_excel(filepath, header = 5)


    L_df = L_df[["Ingredient", "PLM/GAB/NA Spec #", "Item Desc.", L_df.columns[column]]]
    L_df = L_df.dropna(subset = L_df.columns[[0, 3]])

    this_batch = Batch(Path(filepath).parent, Path(filepath).name)
    this_batch.df = L_df

    return this_batch

def main():
    
    column = 8
    batch = readDataTable(db_filepath, column)

    batch.df.to_csv(batch.directory)

if __name__ == '__main__':
    start = time()
    main()
    end = time()
    print(f"Time elapsed; {(end - start) * 1000}ms")
    