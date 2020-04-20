import os, sys, inspect, re, urllib
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import time
from timeit import default_timer as timer
import pyodbc

load_dotenv('.env')

class DBConnector:
    def __init__(self):
        """ Initiate a new database connection. When making a new instance of this function, 
        user will be asked for username and password. Use your Schiphol credentials."""
        params = dict(
            driver = os.environ.get('SQL_ODBC_DRIVER'),\
            server = os.environ.get('AZURE_DB_SERVER'),\
            username = os.environ.get('AZURE_DB_USERNAME'),\
            password = os.environ.get('AZURE_DB_PASSWORD'),\
            database = os.environ.get('AZURE_DB_NAME'),\
            port='35432')
        alchemyParams = urllib.parse.quote_plus(f"DRIVER={os.environ.get('SQL_ODBC_DRIVER')};" + \
                                                f"SERVER={os.environ.get('AZURE_DB_SERVER')};" + \
                                                f"DATABASE={os.environ.get('AZURE_DB_NAME')};" + \
                                                f"UID={os.environ.get('AZURE_DB_USERNAME')};" + \
                                                f"PWD={os.environ.get('AZURE_DB_PASSWORD')}")
        try:
            # two different way to setup db connection
            self.cnxn = pyodbc.connect(driver=params["driver"],
                                       server=params["server"],
                                       port=params["port"],
                                       database=params["database"],
                                       uid=params["username"],
                                       pwd=params["password"]
            )
            self.alchemyEngine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % alchemyParams)
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            print(f"Failed: {sqlstate}")
            self.engine = None
            self.cnxn = None
            self.alchemyEngine = None
    
    def getTables(self):
        """ Call this function to print all tables in the database. A working database connection is required for this."""
        if self.__checkConnection():
            cursor = self.cnxn.cursor()
            for row in cursor.tables():
                print(f"{row[1]} - {row.table_name}")
    
    def getColumns(self, table):
        """ Call this function to print all columns in a given table. A working database connection is required for this."""
        if self.__checkConnection():
            if table is not None:
                cursor = self.cnxn.cursor()
                cursor.execute("SELECT top 0 * FROM %s" % table)
                columns = [column[0] for column in cursor.description]
                for column in columns:   
                    print(column)
            else:
                print("Error: Submit a table when calling this function.")
                
    def runQuery(self, query):
        """ Call this function to execute a SQL query on the database. If successful, the function returns a Pandas DataFrame."""
        print("Starting execution of your query...")
        if self.__checkConnection():
            start_time = timer()
            df = pd.read_sql(query, self.cnxn)
            elapsed_time = timer() - start_time
            print("Finished execution! (Elapsed time: {0:.2f} seconds)".format(elapsed_time))
            return df
        return None
    
    def __checkConnection(self):
        """ Check if the connection is working."""
        if self.cnxn is None:
            print("Error: A working database connection is required to get tables from database.")
            return False
        return True
