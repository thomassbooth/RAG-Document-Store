import os
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings


class VectorStore:

    def __init__(self):
        self._qdrantUrl = os.environ.get("QDRANT_CLIENT")
        self._client = QdrantClient("http://qdrant:6333")

    def store_embeddings(self, embeddings: OpenAIEmbeddings, documentChunks: list[str]):
        """Stores the embeddings in the vector database"""
        try:
            vectorDb = Qdrant.from_documents(
                documentChunks, embeddings, url=self._qdrantUrl, collection_name="test")
        except Exception as error:
            print(f"Error storing embeddings: {error}")
            if isinstance(error, ConnectionError):
                print(
                    "Failed to connect to Qdrant. Please check the server address and network settings.")
            elif isinstance(error, TimeoutError):
                print(
                    "Request to Qdrant timed out. Please check if the server is running and reachable.")
            else:
                print("An unexpected error occurred.")
        return