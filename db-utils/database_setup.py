from pymongo import MongoClient, ASCENDING
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client['dosro']
collection = db['second_hand_products']
# Sample data
data_path = "/home/yg/Documents/new-proj/searchandrec/archive/amazon.csv"
data = pd.read_csv(data_path)
data_dict = data.to_dict(orient='records') 

collection.insert_many(data_dict)
print("Sample data inserted.")


# search_query = "explorers space"
# search_documents(search_query, limit=5)