from fastapi import APIRouter, UploadFile, File, HTTPException
from .embeddings import DocumentProcessor, DocumentEmbedder
from fastapi.responses import StreamingResponse
from concurrent.futures import ThreadPoolExecutor
from .storage import VectorStore
from .retrieval import QueryProcessor

# Create a thread pool for background tasks
executor = ThreadPoolExecutor(max_workers=5)
import io

router = APIRouter()
@router.get("/")
async def test():
    embedder = DocumentEmbedder()
    storage = VectorStore()
    processor = QueryProcessor(embedding_service=embedder, vector_store=storage)
    return StreamingResponse(processor.process_query("Hello"), media_type='text/event-stream')



# Function to process file and call webhook
def process_file_and_notify(contents: bytes, file_name: str):
    embedder = DocumentEmbedder()
    storage = VectorStore()
    processor = DocumentProcessor(embedder, storage)
    documentChunks = processor.document_augmentation(contents, file_name)

@router.post("/upload")
async def upload_and_process_file(file: UploadFile = File(...)):
    """
    Upload a file and read it page by page to generate embeddings.
    """
    try:
        file_name = file.filename
        # Read the file contents into memory
        contents = await file.read()
        executor.submit(process_file_and_notify, contents, file_name)
        return {"File has been processed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
