import pandas as pd
from openpyxl import Workbook
from pathlib import Path

columnNames = {
    "RECIPE"      : "Parent Recipe or Specification",
    "BATCH"       : "Batch",
}
db_filepath = "C:/Users/Paul.Barron/LumiEnv/Lumi/\
files/Stability UCQ Lumisizer DSC Formulation Final_NN.xlsx"
directory = "C:/Users/Paul.Barron/LumiEnv/Lumi/files/"
columns = ["Function", "Sub-Group", "Greg's Name Group", "Ingredient", "Item Desc."]
index_column = "PLM/GAB/NA Spec #"

class Batch:
    def __init__(self, filepath):
        self.path = filepath
        self.directory = Path(filepath).parent
        self.filename = Path(filepath).name
        self.ext = Path(self.filename).suffix
        self.name = self.filename.removesuffix(self.ext)
        self.recipe = {}
        self.meta_data = {}

def read_data_table(filepath, column):
    meta_data_titles = ["Project", "Request ID", "Requestor",
                        "Requester", "Batch or Lot#", "Recipe Description"]
    this_batch = Batch(filepath)
    df = pd.read_excel(filepath, header = None)

    header_row = 5
    
    for i in range(6):
        item = df.iat[i, 0]
        value = str(df.iat[i, column]).strip()
        if item in meta_data_titles:
            this_batch.meta_data.update({df.iat[i, 0]: value})

    df.iat[header_row, column] = request_no = this_batch.meta_data["Request ID"]
    df.columns = df.iloc[header_row]
    columns = ["Ingredient", "PLM/GAB/NA Spec #", "Item Desc.", request_no]
    df = df[columns]
    df = df.dropna(subset = df.columns[[0,3]])
    this_batch.df = df


    return this_batch

def get_ingredients(filepath):
    df = pd.read_excel(filepath, header=5, index_col=5)
    df = df[columns].iloc[:378]
    
    index = [str(x) for x in df.index]
    df.index = list(map(lambda x : x.split('/')[0], index))
    df.dropna(how="all", inplace=True)
    df = df.fillna(method="ffill")

    return df
    
def get_requests(filepath):
    df = pd.read_excel(filepath, header=None)
    

def main():
    df = get_ingredients(db_filepath)
    # print(df.tail(30))
    
    df.to_excel(directory + 'ingredients.xlsx')

if __name__ == '__main__':
    main()


