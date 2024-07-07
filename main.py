from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

import uvicorn

from routes import search

# from src.ranking_algorithm import HybridSearch
# from src.generate_embeddings import CreateEmbeddings 


app = FastAPI(
    description="Hybrid search results"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(search.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  ## make false in production.
    )

# TODO: logic to implement how to create an index.

