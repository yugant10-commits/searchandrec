from http import HTTPStatus
from fastapi import APIRouter
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient, ASCENDING
from typing import Any
from bson import ObjectId

from src.ranking_algorithm import HybridSearch
# from src.generate_embeddings import CreateEmbeddings


router = APIRouter()

def convert_objectid_to_str(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

client = MongoClient('mongodb://localhost:27017/')
db = client['dosro']
collection = db['second_hand_products']
model = SentenceTransformer('all-MiniLM-L6-v2')


@router.get("/api/v1/search", tags=["search"], status_code=HTTPStatus.OK)
async def hybrid_search(
    query:str
):
    """Get search results using hyrbid search"""
    obj = HybridSearch(
        collection=collection, 
        query=query, 
        alpha=0.5, 
        k=10,
        model=model 
        )
    text_results = obj.mongo_text_search()
    vector_results = obj.vector_search()
    combined_results = obj.get_combined_result(text_results, vector_results)
    print("inside api router")
    print(combined_results[0])

    combined_results = convert_objectid_to_str(combined_results)
    print(type(combined_results))
    return combined_results
