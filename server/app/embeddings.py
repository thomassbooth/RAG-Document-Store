import os
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import fitz
from .storage import VectorStore

class DocumentEmbedder:
    """Handles embedding creation and storage."""
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self._embedding_model = OpenAIEmbeddings(api_key=api_key)

    def generate_embeddings(self, paragraphs: list[str]):
        """Handles our call to the OpenAI API to generate embeddings for the paragraphs."""
        try:
            self._embedding_model.embed_documents(paragraphs)
            print(f"Embedding for {len(paragraphs)} paragraphs created.")
        except Exception as e:
            print(f"Error creating embedding: {e}")

    def get_embedding_model(self) -> OpenAIEmbeddings:
        return self._embedding_model

class DocumentProcessor:
    """Handles document processing and augmentation."""
    def __init__(self, embedding_service: DocumentEmbedder, storage_service: VectorStore):
        self._embedding_service = embedding_service
        self._storage_service = storage_service
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=0,
            separators=["\n\n", "\n"]
        )

    def document_augmentation(self, pdf_bytes: bytes, file_name: str):
        """Parses the document page by page, extracts text, creates Document objects with metadata, and generates embeddings."""
        pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_no in range(len(pdf)):
            page = pdf[page_no]
            text = page.get_text("text")
            
            documents = []
            if text:
                paragraphs = self._splitter.split_text(text)
                #add our meta data to each paragraph we are going to store
                for paragraph_no, paragraph in enumerate(paragraphs):
                    metadata = {
                        "source": file_name,
                        "page_index": page_no + 1,
                        "paragraph_index": paragraph_no + 1  
                    }
                    document = Document(page_content=paragraph, metadata=metadata)
                    documents.append(document)

                # Generate embeddings and store for each page
                self._embedding_service.generate_embeddings(paragraphs)
                self._storage_service.store_embeddings(self._embedding_service.get_embedding_model(), documents)

        pdf.close()
