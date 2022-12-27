import os
import pandas as pd
from pathlib import Path
from time import time

start = time()
directory = "//162.87.125.229/trumbull_data/AMS/Lumisizer/Batches/"
# directory = "C:\\Users\\Paul.Barron\\Downloads"
fileTypes = [".csv", ".xlsx"]

files = os.listdir(directory)

columnNames = {
    "RECIPE"      : "Parent Recipe or Specification",
    "BATCH"       : "Batch",
}

class Batch:
    def __init__(self, directory, filename):
        self.path = os.path.join(directory, filename)
        self.filename = filename
        self.ext = Path(self.filename).suffix
        self.name = filename.removesuffix(self.ext)

def isFile(directory, file):
    return os.path.isfile(os.path.join(directory, file))


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
        

def main():
    return

batches = {i: Batch(directory, file) for i, file in enumerate(files)
           if Path(file).suffix in fileTypes}
createDataFrames(batches)

if __name__ == '__main__':
    main()
    end = time()
    print(f"Time elapsed; {(end - start) * 1000}ms")
