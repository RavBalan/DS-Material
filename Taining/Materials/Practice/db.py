from sqlalchemy import create_engine


class sqlDatabase:
    def __init__(self): 
        self.engine = create_engine('mssql+pyodbc://GoveAdmin:gove321admin+@192.129.253.66:1433/Alita-Penske-Document-Dms_20240610?driver=SQL+Server')

    def connection(self):
        return self.engine        