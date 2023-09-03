import psycopg2 as pg
import pandas as pd
from sqlalchemy import create_engine

# configuring the database as created in SQL shell
db_config={
    'dbname':'housing-data',
    'user':'postgres',
    'password':'admin',
    'host':'localhost'
}

conn = pg.connect(**db_config)

engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['dbname']}")

df = pd.read_csv('../cleaned.csv',index_col=[0])
table_name = 'tbl_andheri_housing'
df.to_sql(table_name,engine,if_exists='append',index=False)

conn.close()