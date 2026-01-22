from sqlalchemy import create_engine ,text
import pandas as pd


# Define your connection string
connection_string = "mssql+pyodbc://GoveAdmin:gove321admin+@192.129.253.66:1433/Alita-Penske-Document-Dms_20240610?driver=SQL+Server"

# Create an engine object
engine = create_engine(connection_string)

# Test the connection
connection = engine.connect()
result = connection.execute(text("SELECT top 2 * From DocumentBill")).fetchall()

print(type(result))

df = pd.DataFrame(result)
df.describe()