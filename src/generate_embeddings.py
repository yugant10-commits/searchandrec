from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

class CreateEmbeddings:
    def __init__(
            self, 
            model, 
            collection, 
            column_name: str) -> None:
        self.model = model
        self.collection = collection
        self.data = self.collection.find()
        self.column_name = column_name
    

    def encode_column(self):
        for item in self.data:
            product_name = item['product_name']
            description = item['about_product']
            review_content = item['review_content']
            review_title = item['review_title']
            combined_str = product_name+ " "+ description+ " "+ review_content+ " "+ review_title
            plot_embedding = self.model.encode(combined_str).tolist()
            self.collection.update_one({'_id': item['_id']}, {'$set': {'plot_embedding': plot_embedding}})
            print(f"[INFO] Embeddings created and updated in MongoDB for: {item}")

client = MongoClient('mongodb://localhost:27017/')
db = client['dosro']
collection = db['second_hand_products']

CreateEmbeddings(
    model = SentenceTransformer('all-MiniLM-L6-v2'), 
    collection=collection, 
    column_name=""
).encode_column()
collection.create_index(
    [("product_name", "text"), ("review_content", "text")],
    default_language='english'
)
