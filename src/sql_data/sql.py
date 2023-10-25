import os
import pandas as pd
import sqlite3
from sqlite3 import Error
from pathlib import Path

os.listdir()
os.chdir('src\sql_data')
sql_dir = os.path.join(Path(__file__).parents[0])

class SQL:
    '''
    Create a connection to the sqlite database.
    uploadSQL is a simple replace upload statement using
    pandas to easily build the tables where they dont exist.
    future idea would be to create a seperate update function 
    to update if exists or append if not
    '''
    def __init__(self) -> None:
        self.conn = sqlite3.connect('pantryplan.db')
        self.cur = self.conn.cursor()
    

    def uploadSQL(self,csv,table)->None:
        print(f'{sql_dir}\{csv}')
        self.df=pd.read_csv(f'{sql_dir}\{csv}')
        try:
            
            self.df.to_sql(table,self.conn,if_exists='replace',index=False)
        except:
            print(f"upload to {table} unsuccessful")

if __name__ == '__main__':
    p= SQL()
    cursor=p.cur
    '''one time insert into databse to create tables from our scraped tables'''
    #p.uploadSQL('recipe_ingredients.csv',"recipe_ingredients")
    #p.uploadSQL('recipe_nutrition.csv',"recipe_nutrition")
    #p.uploadSQL('recipe_steps.csv',"recipe_steps")
    #p.uploadSQL('recipe_times.csv',"recipe_times")
    #p.uploadSQL('recipes.csv',"recipes")
    #df=pd.read_sql("select * from recipes",p.conn)
    cursor.close()


