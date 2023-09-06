import psycopg2 as pg
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import types, MetaData,Table, Column, PrimaryKeyConstraint, UniqueConstraint
from Constants.constants import POSTGRES_DTYPES

# configuring the database as created in SQL shell
class inputTableToPostgres():
    def __init__(self):
        pass
    def input_table(self,df):
        try:
            conn = pg.connect(
                user="postgres",
                password="admin",
                host="localhost",
                port="5433",
                database="postgres"
            )
            print("Connected to the database successfully")
        except (Exception, pg.Error) as e:
            print("Error while connecting to PostgreSQL", e)

        engine = create_engine(f"postgresql://postgres:admin@localhost:5433/postgres")

        table_name = 'tbl_andheri_housing'
        df.to_sql(table_name,engine,if_exists='append',index=False, dtype=POSTGRES_DTYPES)
        print('input into database successful')
        # add constraints to the table when adding for the first time
        conn.close()