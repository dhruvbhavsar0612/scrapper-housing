import psycopg2 as pg
import pandas as pd
from sqlalchemy import create_engine

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
        df.to_sql(table_name,engine,if_exists='append',index=False)

        conn.close()