import pandas as pd

env_folder                      = "C:/Users/Paul.Barron/LumiEnv/Lumi/"
files_fp                        = "C:/Users/Paul.Barron/LumiEnv/Lumi/files/"
old_datatable_filename          = "Lumi_DB.xlsx"
old_datatable_output_filename   = "db_recipes.csv"
lims_datatable_filename         = "lims_recipes.xls"
lims_recipe_modified            = "lims_recipes_modified.csv"
full_recipe_list_filename       = "full_recipe_list.csv"
nn_filename                     = "nearest_neighbor.csv"

def pd_settings():
    options = {
        'display': {
            'max_columns': 20,
            'max_colwidth': 20,
            'expand_frame_repr': False,
            'max_rows': 30,
            'max_seq_items': 50,
            'precision': 4,
            'show_dimensions': False,
        },
        'mode': {
            'chained_assignment': None,
        }
    }

    for category, option in options.items():
        for op, value in option.items():
            pd.set_option(f'{category}.{op}', value)