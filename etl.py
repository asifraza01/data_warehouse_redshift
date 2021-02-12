import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Load JSON input data from S3 and insert
        into staging_events and staging_songs tables.
    Keyword arguments:
    * cur --    reference to connected db.
    * conn --   connect the DB.
    Output:
    * staging tables.
    """
        
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
     """Insert data from staging tables to fact and dimension tables:
    Keyword arguments:
    * cur --    reference to connected db.
    * conn --   connect the DB.
    Output:
    * Data inserted from staging to dimension and fact tables.

    """    
    
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Connect to DB
    Keyword arguments:
    * None
    Output:
    * All ETL processed in DB tables.
    """
    
    
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()