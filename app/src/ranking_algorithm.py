import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors."""
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def rrf_score(rank, k):
    """Calculate the reciprocal rank fusion score."""
    return 1 / (rank + k)

class HybridSearch:
    def __init__(self, collection: MongoClient, query: str, alpha: float, k: int, model: SentenceTransformer) -> None:
        self.collection = collection
        self.query = query
        self.alpha = alpha
        self.model = model
        self.k = k
        self.all_docs = list(self.collection.find({}, {'_id': 1, 'plot_embedding': 1}))
        self.query_embedding = self.model.encode(self.query).tolist()

    def vector_search(self) -> list:
        """Perform vector search."""
        vector_search_results = [
            (doc['_id'], cosine_similarity(self.query_embedding, doc['plot_embedding']))
            for doc in self.all_docs
        ]
        vector_search_results.sort(key=lambda x: x[1], reverse=True)
        return vector_search_results[:self.k]

    def mongo_text_search(self) -> list:
        """Perform MongoDB text search."""
        text_search_results = list(self.collection.find(
            {'$text': {'$search': self.query}},
            {'score': {'$meta': 'textScore'}}
        ).sort([('score', {'$meta': 'textScore'})]).limit(self.k))
        return text_search_results

    def get_combined_result(self, text_search_results: list, vector_search_results: list) -> list:
        """Combine vector search and text search results."""
        combined_results = {}
        for idx, (doc_id, _) in enumerate(vector_search_results):
            combined_results[doc_id] = combined_results.get(doc_id, 0) + self.alpha * rrf_score(idx + 1, self.k)
        for idx, result in enumerate(text_search_results):
            combined_results[result['_id']] = combined_results.get(result['_id'], 0) + (1 - self.alpha) * rrf_score(idx + 1, self.k)

        sorted_results = sorted(combined_results.items(), key=lambda x: x[1], reverse=True)

        # Retrieve full documents and include only specified columns
        final_results = []
        for doc_id, score in sorted_results:
            doc = self.collection.find_one({'_id': doc_id}, {'product_name': 1, 'actual_price': 1, 'product_id': 1, 'user_name': 1, 'review_title': 1})
            if doc:
                doc['combined_score'] = score
                final_results.append(doc)
        
        return final_results[:self.k]

# Example usage
# mongo_client = MongoClient('mongodb://localhost:27017/')
# collection = mongo_client['mydatabase']['mycollection']
# model = SentenceTransformer('all-MiniLM-L6-v2')
# hybrid_search = HybridSearch(collection, "sample query", 0.5, 10, model)
# vector_results = hybrid_search.vector_search()
# text_results = hybrid_search.mongo_text_search()
# final_results = hybrid_search.get_combined_result(text_results, vector_results)
