import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

filepath = "C:/Users/Paul.Barron/LumiEnv/Lumi/files/"
requests_filepath = filepath + "Requests.csv"
samples_filepath = filepath + "Samples.csv"

reqs = ["R-20221121-00030"]

requests = pd.read_csv(requests_filepath)
requests["Recipe / Alternate / Version"] = requests["Recipe / Alternate / Version"].apply(lambda x: str(x))
# still exponential notation


samples = pd.read_csv(samples_filepath)
print(requests.head(100))
samples = samples.merge(requests, on="Request", how="left")


#samples.to_csv(filepath + "output.csv")
