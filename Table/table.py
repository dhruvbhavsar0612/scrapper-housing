import psycopg2 as pg
<<<<<<< HEAD

# configuring the database as created in SQL shell
db_config={
    'dbname':'housing-data',
    'user':'postgres',
    'password':'admin',
    'host':'localhost'
}

conn = pg.connect(**db_config)

# creating cursor object - helpful for interacting with database
cursor = conn.cursor()

create_table_sql = """
    CREATE TABLE IF NOT EXISTS tbl_main (
        
    );
"""
=======
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import types, MetaData,Table, Column, PrimaryKeyConstraint, UniqueConstraint
from Constants.constants import POSTGRES_DTYPES

# configuring the database as created in SQL shell
class inputTableToPostgres():
    def __init__(self):
        pass
    def input_table(self,count):
        try:
            conn = pg.connect(
                user="postgres",
                password="admin",
                host="localhost",
                port="5433",
                database="postgres"
            )
            cursor = conn.cursor()
            print("Connected to the database successfully")
        except (Exception, pg.Error) as e:
            print("Error while connecting to PostgreSQL", e)

        engine = create_engine(f"postgresql://postgres:admin@localhost:5433/postgres")

        df = pd.read_csv(f'./cleaned_{count}.csv',index_col=[0])
        table_name = 'tbl_andheri_housing'
        df.to_sql(table_name,engine,if_exists='append',index=False, dtype=POSTGRES_DTYPES)
        
        # add constraints to the table when adding for the first time
        conn.close()
>>>>>>> bdc53be12ff0768043ffdab7dbb740668f72183c
