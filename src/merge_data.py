from pathlib import Path
import pandas as pd
import os


sql_dir = os.path.join(Path(__file__).parents[0], 'sql_data')

rec_dir = os.path.join(Path(__file__).parents[0], '1_recipe_data')
ing_dir = os.path.join(Path(__file__).parents[0], '2_ingredients_data')
stp_dir = os.path.join(Path(__file__).parents[0], '3_steps_data')

def mergeFiles(directory,table=''):
    #create empty dataframe to append into
    df_table =pd.DataFrame()
    #empty list to get file paths
    file_paths = []
    # Walk through the directory and its subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Get the full file path
            file_path = os.path.join(root, filename)
            # Append the file path to the list
            file_paths.append(file_path)

    # Now, file_paths contains all the file paths in the specified folder and its subdirectories
    for file in file_paths:
        df_temp =pd.read_csv(file)
        df_table = pd.concat([df_table,df_temp],ignore_index=True)
        print(f'{file} data has been appended')
    df_table.to_csv(f'{sql_dir}\{table}.csv',index=False)
    print(f'{table} successfully built!')
    
#--------------execute function merge all data-----------
mergeFiles(rec_dir,"recipes")
#mergeFiles(ing_dir,"recipe_ingredients")
#mergeFiles(stp_dir,"recipe_steps")