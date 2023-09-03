import psycopg2 as pg

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